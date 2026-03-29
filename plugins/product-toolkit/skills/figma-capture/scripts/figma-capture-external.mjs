#!/usr/bin/env node

/**
 * figma-capture-external.mjs
 *
 * 외부 URL을 Chrome CDP로 열고 Figma capture.js를 주입하여 캡처합니다.
 * Node.js v22+ 내장 WebSocket 사용 — npm install 불필요.
 *
 * Usage:
 *   node figma-capture-external.mjs --url <https://...> --capture-id <captureId> [--port 9222] [--timeout 30]
 *
 * 동작 흐름:
 *   1. Chrome을 --remote-debugging-port로 실행 (이미 실행 중이면 기존 인스턴스 사용)
 *   2. CDP로 새 탭을 열어 외부 URL 탐색
 *   3. 페이지 로드 완료 후 capture.js 주입
 *   4. window.figma.captureForDesign({captureId, endpoint, selector}) fire-and-forget 호출
 *   5. 15초 대기 후 종료 (캡처 데이터 네트워크 전송 완료 대기)
 */

import fs from "node:fs";
import http from "node:http";
import { spawn } from "node:child_process";
import { platform } from "node:os";
import { parseArgs as nodeParseArgs } from "node:util";

// ── Args ──

function parseArgs() {
  try {
    const { values } = nodeParseArgs({
      options: {
        url: { type: "string" },
        "capture-id": { type: "string" },
        port: { type: "string", default: "9222" },
        timeout: { type: "string", default: "30" },
        "no-headless": { type: "boolean", default: false },
      },
    });

    const parsed = {
      url: values.url,
      captureId: values["capture-id"],
      port: Number(values.port),
      timeout: Number(values.timeout),
      headless: !values["no-headless"],
    };

    if (!parsed.url || !parsed.captureId) {
      throw new Error("Missing required arguments: --url and --capture-id");
    }
    return parsed;
  } catch (err) {
    console.error(`Error: ${err.message}`);
    console.error(
      "Usage: node figma-capture-external.mjs --url <URL> --capture-id <captureId> [--port 9222] [--timeout 30] [--no-headless]"
    );
    process.exit(1);
  }
}

const { url, captureId, port, timeout, headless } = parseArgs();

// ── Chrome launcher ──

function getChromePath() {
  const os = platform();
  if (os === "darwin") {
    return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  }
  if (os === "win32") {
    const paths = [
      "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
      "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    ];
    for (const p of paths) {
      if (fs.existsSync(p)) return p;
    }
  }
  // Linux fallback
  return "google-chrome";
}

function isChromeDebugging(debugPort) {
  return new Promise((resolve) => {
    const req = http.request({ hostname: "127.0.0.1", port: debugPort, path: "/json/version", method: "GET" }, (res) => {
      let d = "";
      res.on("data", (c) => (d += c));
      res.on("end", () => {
        try {
          const info = JSON.parse(d);
          resolve(typeof info.Browser === "string" && info.Browser.includes("Chrome"));
        } catch {
          resolve(false);
        }
      });
    });
    req.on("error", () => resolve(false));
    req.end();
  });
}

async function launchChrome(debugPort) {
  if (await isChromeDebugging(debugPort)) {
    console.log(`Chrome already running on port ${debugPort}`);
    return { process: null, launchedByUs: false };
  }
  console.log("Launching Chrome with remote debugging...");
  const chromeArgs = [
    `--remote-debugging-port=${debugPort}`,
    "--no-first-run",
    "--no-default-browser-check",
    "--user-data-dir=" + (platform() === "win32" ? `${process.env.TEMP || process.env.TMP || "C:\\Temp"}\\figma-cdp` : "/tmp/figma-cdp"),
  ];
  if (headless) chromeArgs.push("--headless=new");
  chromeArgs.push("about:blank");

  const chrome = spawn(getChromePath(), chromeArgs, { stdio: "ignore", detached: true });
  chrome.unref();

  // Wait for CDP to be ready
  for (let i = 0; i < 20; i++) {
    await sleep(500);
    if (await isChromeDebugging(debugPort)) return { process: chrome, launchedByUs: true };
  }
  throw new Error("Chrome failed to start with remote debugging");
}

// ── CDP helpers ──

function httpRequest(endpoint, method = "GET") {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(endpoint);
    const opts = { hostname: urlObj.hostname, port: urlObj.port, path: urlObj.pathname + urlObj.search, method };
    const req = http.request(opts, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => { try { resolve(JSON.parse(data)); } catch (e) { reject(new Error(`Invalid JSON: ${data.slice(0, 100)}`)); } });
    });
    req.on("error", reject);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

class CDPSession {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this._id = 0;
    this._callbacks = new Map();
    this._events = new Map();

    this.ws.addEventListener("message", (evt) => {
      const msg = JSON.parse(evt.data);
      if (msg.id !== undefined && this._callbacks.has(msg.id)) {
        this._callbacks.get(msg.id)(msg);
        this._callbacks.delete(msg.id);
      }
      if (msg.method && this._events.has(msg.method)) {
        const handlers = this._events.get(msg.method);
        for (const h of handlers) h(msg.params);
      }
    });
  }

  ready() {
    return new Promise((resolve, reject) => {
      this.ws.addEventListener("open", resolve);
      this.ws.addEventListener("error", reject);
    });
  }

  send(method, params = {}) {
    const id = ++this._id;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this._callbacks.delete(id);
        reject(new Error(`CDP timeout: ${method}`));
      }, timeout * 1000);

      this._callbacks.set(id, (msg) => {
        clearTimeout(timer);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  once(eventName) {
    return new Promise((resolve) => {
      const handler = (params) => {
        const handlers = this._events.get(eventName);
        if (handlers) {
          const idx = handlers.indexOf(handler);
          if (idx >= 0) handlers.splice(idx, 1);
        }
        resolve(params);
      };
      if (!this._events.has(eventName)) this._events.set(eventName, []);
      this._events.get(eventName).push(handler);
    });
  }

  close() {
    this.ws.close();
  }
}

// ── Main ──

async function main() {
  // 1. Launch Chrome
  const chrome = await launchChrome(port);
  let cdp = null;
  let targetId = null;

  try {
    // 2. Create a new tab with the target URL (Chrome 130+ requires PUT)
    const newTarget = await httpRequest(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(url)}`, "PUT");
    targetId = newTarget.id;
    const wsUrl = newTarget.webSocketDebuggerUrl;
    if (!wsUrl) throw new Error("No webSocketDebuggerUrl returned");

    console.log(`Navigating to: ${url}`);
    cdp = new CDPSession(wsUrl);
    await cdp.ready();

    // 3. Enable Page events & wait for load
    await cdp.send("Page.enable");

    // If the page is still loading, wait for load event
    // Give a grace period for already-loaded pages
    const loadPromise = cdp.once("Page.loadEventFired");
    const frameResult = await cdp.send("Page.getFrameTree");
    const mainFrameUrl = frameResult?.frameTree?.frame?.url;

    if (!mainFrameUrl || mainFrameUrl === "about:blank" || mainFrameUrl === "") {
      // Page hasn't navigated yet — navigate
      await cdp.send("Page.navigate", { url });
      await loadPromise;
    } else {
      // New tab already navigated — wait briefly or check if loaded
      await Promise.race([loadPromise, sleep(3000)]);
    }
    console.log("Page loaded");

    // 4. Remove CSP headers that might block script injection
    await cdp.send("Page.setBypassCSP", { enabled: true });

    // 5. Inject capture.js via fetch + eval (bypasses CSP issues with <script> tags)
    console.log("Injecting capture.js...");
    await cdp.send("Runtime.evaluate", {
      expression: `
        fetch('https://mcp.figma.com/mcp/html-to-design/capture.js')
          .then(r => r.text())
          .then(code => {
            const script = document.createElement('script');
            script.textContent = code;
            document.head.appendChild(script);
          })
      `,
      awaitPromise: true,
      returnByValue: true,
    });

    // 6. Wait for window.figma.captureForDesign to be available
    console.log("Waiting for capture.js to initialize...");
    const safeCaptureId = JSON.stringify(captureId);
    const safeEndpoint = JSON.stringify(`https://mcp.figma.com/mcp/capture/${captureId}/submit`);

    const checkResult = await cdp.send("Runtime.evaluate", {
      expression: `
        new Promise((resolve) => {
          let attempts = 0;
          const check = setInterval(() => {
            attempts++;
            if (window.figma && typeof window.figma.captureForDesign === 'function') {
              clearInterval(check);
              resolve('ready');
            } else if (attempts > 50) {
              clearInterval(check);
              resolve('not_found');
            }
          }, 100);
        })
      `,
      awaitPromise: true,
      returnByValue: true,
    });

    if (checkResult?.result?.value === "not_found") {
      throw new Error("window.figma.captureForDesign not available after 5s");
    }

    // Fire-and-forget: captureForDesign의 Promise는 resolve되지 않으므로 await하지 않음
    console.log(`Firing captureForDesign({ captureId: ${safeCaptureId} })...`);
    await cdp.send("Runtime.evaluate", {
      expression: `
        (() => {
          const captureId = ${safeCaptureId};
          const endpoint = ${safeEndpoint};
          window.figma.captureForDesign({
            captureId: captureId,
            endpoint: endpoint,
            selector: 'body'
          })
            .then(() => console.log('figma-capture: submitted'))
            .catch(e => console.error('figma-capture error:', e));
        })()
      `,
      awaitPromise: false,
      returnByValue: true,
    });

    // 캡처 데이터 전송 대기 (네트워크 요청 완료까지)
    console.log("Waiting 15s for capture data submission...");
    await sleep(15000);
    console.log("Capture submitted.");
  } finally {
    // Cleanup: close tab, CDP connection, and Chrome (if we launched it)
    if (targetId) {
      await httpRequest(`http://127.0.0.1:${port}/json/close/${targetId}`, "PUT").catch(() => {});
    }
    if (cdp) {
      cdp.close();
    }
    if (chrome.launchedByUs && chrome.process) {
      chrome.process.kill();
      console.log("Chrome process terminated.");
    }
    console.log("Done.");
  }
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
