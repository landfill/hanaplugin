# 이벤트 레지스트리 (경량)

> 이 파일은 2-0단계(이벤트 레지스트리 조회)에서 **항상 로드**된다.
> 공유 이벤트 판정 + 구분 프로퍼티 스키마를 제공한다.

---

## 공유 이벤트 규칙

아래 이벤트는 해당 페이지의 **모든 액션이 동일 이벤트를 공유**하며,
각 이벤트에 지정된 **구분 프로퍼티**로 개별 액션을 구분한다.
이 페이지에 새 액션이 추가될 경우 **새 이벤트를 만들지 않고** 기존 이벤트를 사용하고,
해당 이벤트의 구분 프로퍼티에 새 value를 추가한다.

> **주의**: 구분 프로퍼티는 이벤트마다 다르다. 반드시 아래 프로퍼티 정의 섹션을 참조할 것.

| Event Name (EN) | Event Name (KR) | PC/MO | 1 Depth | 2 Depth | 3 Depth | 구분 프로퍼티 |
|--|--|--|--|--|--|--|
| button_click_pkg_pay | 패키지 결제페이지 내 버튼클릭 | ALL | 해외여행 | 상품 페이지 | 결제페이지 | buttonCatg, buttonNm |
| button_click_pkg_pay_finish | 패키지 결제완료 페이지 내 버튼클릭 | ALL | 해외여행 | 상품 페이지 | 결제페이지 | buttonCatg, buttonNm |
| button_click_pkg_reservation | 패키지 예약하기 페이지 내 버튼클릭 | ALL | 해외여행 | 상품 페이지 | 예약페이지 | buttonCatg, buttonNm |
| button_click_pkg_reservation_detail | 패키지 예약 상세페이지 버튼 | MO | 해외여행 | 상품 페이지 | 예약페이지 | buttonCatg, buttonNm |
| button_click_pkg_reservation_detail_info | 패키지 예약내역상세 내 버튼클릭 | ALL | 해외여행 | 상품 페이지 | 예약페이지 | buttonCatg, buttonNm |
| button_click_pkg_reservation_finish | 패키지(국내) 예약완료 페이지 내 버튼클릭 | ALL | 해외여행 | 상품 페이지 | 예약페이지 | buttonCatg, buttonNm |

---

## 공유 이벤트 프로퍼티 정의

> 전역 프로퍼티(bSessionId, isLogin, locationPathname, prePage, resPathCd 등)는
> SKILL.md 전역 제외 규칙에 따라 생략. 아래는 각 이벤트의 **구분 프로퍼티만** 기재.

### button_click_pkg_pay

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 할인혜택, 마일리지 조회 등 | 버튼 카테고리 |
| buttonNm | 기존 | 조회하기, 적용하기 등 | 버튼명 |

### button_click_pkg_pay_finish

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 여행자정보 등 | 버튼 카테고리 |
| buttonNm | 기존 | 여행자정보 입력, 예약내역 보기 등 | 버튼명 |

### button_click_pkg_reservation

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 항공정보, 이용호텔, 선택관광 등 | 버튼 카테고리 |
| buttonNm | 기존 | 상세보기, 변경하기 등 | 버튼명 |

### button_click_pkg_reservation_detail

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 여행자정보 등 | 버튼 카테고리 |
| buttonNm | 기존 | 여권촬영등록, 확인하기 등 | 버튼명 |

### button_click_pkg_reservation_detail_info

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 호텔상세, 선택관광 등 | 버튼 카테고리 |
| buttonNm | 기존 | 상세보기, 선택하기 등 | 버튼명 |

### button_click_pkg_reservation_finish

| Event property | property 구분 | value | description |
|--|--|--|--|
| buttonCatg | 기존 | 예약내역, 여행자정보 등 | 버튼 카테고리 |
| buttonNm | 기존 | 예약내역 보기, 여행자정보 입력 등 | 버튼명 |

---

## 변경 이력

| 날짜 | 내용 | 작성자 |
|--|--|--|
| 2026.03.25 | 초안 생성 (공유 이벤트 6개 규칙 + 구분 프로퍼티) | - |
| 2026.03.25 | Navigation 컬럼 제거, 1Depth 기준 매칭으로 전환 | - |
