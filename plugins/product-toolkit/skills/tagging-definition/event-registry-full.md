# 전체 이벤트 목록 (1Depth 기준)

> 이 파일은 `event-registry.md`에서 공유 이벤트 미매칭 시에만 참조한다.
> 동일 1Depth의 기존 이벤트를 검색하여 중복 여부를 확인하는 용도.

---

## 해외여행·패키지 (35건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 82 | ALL | shopping_cart_add_pkg | 찜 _ 패키지 | 패키지 | 상품 페이지 | 찜 | CLICK |
| 84 | ALL | shopping_cart_add_pkg_popup | 찜 _ 팝업 추천 클릭(패키지) | 패키지 | 상품 페이지 | 찜_팝업 | CLICK |
| 199 | MO | clicked_detail_pkg_rcmn_pkg | 패키지상품_추천 패키지상품 상세보기 | 패키지 상품 | 추천 패키지 상품 |  | CLICK |
| 119 | ALL | smn_pkg_md | 서브홈_패키지 > MD추천상품 | 해외여행 | MD 추천 |  | CLICK |
| 118 | ALL | smn_pkg_mdpage | 서브홈_패키지 > 기획전 | 해외여행 | 기획전 |  | CLICK |
| 106 | MO | view_detail_pkg_rppd | 서브홈_패키지 > 대표상품상세보기 | 해외여행 | 대표상품 |  | CLICK |
| 107 | MO | view_detail_pkg_rppd_rebrowsing | 서브홈_패키지 > 대표상품상세보기(재검색) | 해외여행 | 대표상품 | 재검색 | CLICK |
| 108 | MO | view_detail_pkg_slpd | 서브홈_패키지 > 판매상품상세보기 | 해외여행 | 대표상품 | 판매상품 | CLICK |
| 109 | MO | view_detail_pkg_slpd_rebrowsing | 서브홈_패키지 > 판매상품상세보기(재검색) | 해외여행 | 대표상품 | 판매상품_재검색 | CLICK |
| 111 | ALL | load_detail_pkg | 패키지상품 상세 페이지 | 해외여행 | 상품 페이지 |  | LOAD |
| 56 | ALL | pay_finish_pkg | 결제완료 (패키지) | 해외여행 | 상품 페이지 | 결제 | LOAD |
| 63 | ALL | button_click_pkg_pay | 패키지 결제페이지 내 버튼클릭 | 해외여행 | 상품 페이지 | 결제페이지 | CLICK |
| 64 | ALL | button_click_pkg_pay_finish | 패키지 결제완료 페이지 내 버튼클릭 | 해외여행 | 상품 페이지 | 결제페이지 | CLICK |
| 69 | ALL | load_pages_pkg_pay | 결제페이지 페이지로드 | 해외여행 | 상품 페이지 | 결제페이지 | LOAD |
| 70 | ALL | load_pages_pkg_pay_finish | 결제완료페이지 페이지로드 | 해외여행 | 상품 페이지 | 결제페이지 | LOAD |
| 55 | ALL | view_itinerary_pkg | 패키지 상품페이지 다른출발일선택/출발일항공편 변경 | 해외여행 | 상품 페이지 | 다른출발일 | CLICK |
| 65 | ALL | button_click_pkg_reservation | 패키지 예약하기 페이지 내 버튼클릭 | 해외여행 | 상품 페이지 | 예약페이지 | CLICK |
| 66 | MO | button_click_pkg_reservation_detail | 패키지 예약 상세페이지 버튼 | 해외여행 | 상품 페이지 | 예약페이지 | CLICK |
| 67 | ALL | button_click_pkg_reservation_detail_info | 패키지 예약내역상세 내 버튼클릭 | 해외여행 | 상품 페이지 | 예약페이지 | CLICK |
| 68 | ALL | button_click_pkg_reservation_finish | 패키지(국내) 예약완료 페이지 내 버튼클릭 | 해외여행 | 상품 페이지 | 예약페이지 | CLICK |
| 71 | ALL | load_pages_pkg_reservation | 페이지로드 (예약하기 페이지) | 해외여행 | 상품 페이지 | 예약페이지 | LOAD |
| 72 | MO | load_pages_pkg_reservation_detail | 페이지로드 (여행자 정보입력) | 해외여행 | 상품 페이지 | 예약페이지 | LOAD |
| 73 | ALL | load_pages_pkg_reservation_detail_info | 페이지로드 (예약내역상세) | 해외여행 | 상품 페이지 | 예약페이지 | LOAD |
| 74 | ALL | load_pages_pkg_reservation_finish | 페이지로드 (예약완료) | 해외여행 | 상품 페이지 | 예약페이지 | LOAD |
| 78 | ALL | reservation_click_pkg | 패키지 예약하기 클릭 | 해외여행 | 상품 페이지 | 예약페이지 | CLICK |
| 49 | ALL | view_comparison_add_pkg | 상품비교함담기(패키지) | 해외여행 | 상품비교함담기 |  | CLICK |
| 50 | ALL | view_comparison_pkg | 패키지상품비교하기 | 해외여행 | 상품비교함담기 | 상품비교하기 | CLICK |
| 117 | PC | smn_search_pkg | 서브홈_패키지 > 검색 | 해외여행 | 패키지 검색 |  | CLICK |
| 114 | MO | smn_search_pkg_simple | 서브홈_패키지 > 날짜조회 | 해외여행 | 패키지검색 | 날짜조회 | CLICK |
| 187 | MO | smn_search_pkg_detail | 서브홈_패키지 > 상세필터 | 해외여행 | 패키지검색 | 상세필터 |  |
| 113 | MO | smn_search_pkg_fiter | 서브홈_패키지 > 필터검색 | 해외여행 | 패키지검색 결과 | 필터조회 | CLICK |
| 51 | ALL | view_detail_pkg | 상세보기(패키지) | 해외여행 | 패키지상품 상세 | 상품 페이지 | CLICK |
| 58 | ALL | pay_finish_air | 결제완료 (항공) | 해외여행 | 항공 페이지 | 결제 | LOAD |
| 59 | ALL | reservation_finish_air | 예약완료(항공) | 해외여행 | 항공 페이지 | 예약하기 | LOAD |
| 57 | ALL | pay_finish_hotel | 결제완료 (호텔) | 해외여행 | 호텔 페이지 | 결제 | LOAD |

---

## 호텔 (20건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 104 | ALL | smn_hotel_md | 서브홈_호텔 > MD추천상품 | 호텔 | MD추천 |  | CLICK |
| 100 | ALL | smn_search_hotel | 서브홈_호텔 > 검색 | 호텔 | 검색 |  | CLICK |
| 135 | ALL | smn_pkg_banner | 패키지서브홈_배너 | 호텔 | 국내호텔 | 배너 | CLICK |
| 101 | ALL | smn_hotel_mdpage | 서브홈_호텔 > 기획전 | 호텔 | 기획전 |  | CLICK |
| 46 | ALL | view_comparison_add_hotel | 상품비교함담기(호텔) | 호텔 | 비교 |  | CLICK |
| 47 | ALL | view_comparison_hotel | 숙소 비교하기_호텔비교 | 호텔 | 숙소비교하기 |  | CLICK |
| 48 | ALL | view_comparison_detail_hotel | 숙소비교하기_상세보기 클릭 | 호텔 | 숙소비교하기 | 상세보기 | CLICK |
| 102 | ALL | smn_htl_recent | 서브홈_호텔 > 최근 검색 클릭 | 호텔 | 최근 검색 |  | CLICK |
| 103 | ALL | smn_hotel_tabarea | 서브홈_호텔 > 탭영역 클릭 | 호텔 | 탭영역 |  | CLICK |
| 112 | ALL | load_detail_htlcode | 호텔상품 상세 페이지 | 호텔 | 호텔 페이지 |  | LOAD |
| 110 | ALL | load_detail_htl | 페이지로드 _ 호텔 예약하기 | 호텔 | 호텔 페이지 | 예약 | CLICK |
| 75 | ALL | agreement_click | 호텔_모든약관 동의 클릭 | 호텔 | 호텔 페이지 | 예약페이지 | CLICK |
| 76 | ALL | agreement_yn | 호텔_예약취소 및 환불정책 | 호텔 | 호텔 페이지 | 예약페이지 | CLICK |
| 77 | ALL | reservation_click_htl | 호텔 예약하기 클릭 | 호텔 | 호텔 페이지 | 예약페이지 | CLICK |
| 83 | ALL | shopping_cart_add_hotel | 장바구니(호텔) | 호텔 | 호텔 페이지 | 찜 | CLICK |
| 85 | ALL | shopping_cart_add_hotel_popup | 찜 _ 팝업 추천 클릭(호텔) | 호텔 | 호텔 페이지 | 찜_팝업 | CLICK |
| 99 | PC | smn_hotel_review | 이용후기탭클릭 | 호텔 | 호텔상세 | 숙소후기 | CLICK |
| 52 | ALL | view_detail_hotel | 상세보기(호텔) | 호텔 | 호텔상품 상세 | 호텔 페이지 | CLICK |
| 185 | ALL | smn_htl_banner | 서브홈_호텔 > 롱배너 | 호텔 서브 | 롱배너 |  | CLICK |
| 186 | MO | smn_htl_md | 서브홈_호텔 > 추천 호텔 | 호텔 서브 | 추천 호텔 |  | CLICK |

---

## 항공 (12건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 219 | ALL | reservation_finish_air_rcmn | 항공 예약 시 추천상품 | 항공 |  |  |  |
| 130 | ALL | smn_air_md | 항공 서브_MD추천상품 | 항공 | MD추천 |  | CLICK |
| 127 | ALL | smn_search_air | 항공 서브_검색 | 항공 | 검색 |  | CLICK |
| 128 | ALL | smn_air_mdpage | 항공 서브_기획전 | 항공 | 기획전 |  | CLICK |
| 131 | ALL | smn_air_banner | 항공 서브_배너 | 항공 | 배너 |  | CLICK |
| 218 | ALL | reservation_click_air | 항공_예약 | 항공 | 요금선택(버튼) | 예약하기 | CLICK |
| 220 | ALL | reservation_next_air | 항공_예약 | 항공 | 요금선택(버튼) | 예약하기 | CLICK |
| 129 | ALL | smn_air_recent | 항공 서브_최근 검색 | 항공 | 최근 검색 |  | CLICK |
| 196 | MO | air_reservation_pageBack | 항공권 상세 버튼(뒤로가기) | 항공 | 항공 상품 페이지 | 항공권 상세 버튼 | CLICK |
| 184 | MO | smn_air_notice | 서브홈_항공 > 공지 | 항공 서브 | 공지 |  | CLICK |
| 54 | ALL | view_detail_rt_air | 상세보기(항공-왕복) | 해외항공 | 왕복항공 상세 | 항공 페이지 | CLICK |
| 53 | ALL | view_detail_ow_air | 상세보기(항공-편도) | 해외항공 | 편도항공 상세 | 항공 페이지 | CLICK |

---

## 마이페이지 (33건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 149 | MO | mypage_myplanner | 마이페이지 MY 플래너 | 마이페이지 | MY 플래너 |  | CLICK |
| 20 | ALL | mypage_q&a | 마이페이지_1:1 게시판 문의내역 | 마이페이지 | Q&A |  | CLICK |
| 25 | ALL | mypage_privacy | 마이페이지_개인정보 | 마이페이지 | 개인정보수정 |  | CLICK |
| 26 | ALL | delete_account | 회원탈퇴 | 마이페이지 | 개인정보수정 | 회원탈퇴 | CLICK |
| 27 | ALL | delete_account_finish | 회원탈퇴 완료후 | 마이페이지 | 개인정보수정 | 회원탈퇴 | LOAD |
| 24 | ALL | mypage_quote | 마이페이지_견적문의내역 | 마이페이지 | 견적문의 |  | CLICK |
| 150 | MO | mypage_reservation_air | 마이페이지 국내항공 | 마이페이지 | 국내항공 |  | CLICK |
| 22 | ALL | mypage_review | 마이페이지_My상품평 | 마이페이지 | 리뷰 |  | CLICK |
| 17 | ALL | mypage_mileage | 마이페이지_마일리지 | 마이페이지 | 마일리지 |  | CLICK |
| 146 | MO | mileage_useExits | 마이페이지_마일리지 > 소멸예정 조회 | 마이페이지 | 마일리지 | 소멸예정 마일리지 | CLICK |
| 148 | MO | mypage_banner | 마이페이지 배너 | 마이페이지 | 배너 |  | CLICK |
| 18 | ALL | mypage_giftcard | 마이페이지_상품권 | 마이페이지 | 상품권 |  | CLICK |
| 30 | ALL | service_mileage | 서비스_마일리지 | 마이페이지 | 서비스 마일리지 |  | CLICK |
| 28 | ALL | service_shopping_cart | 서비스_장바구니 | 마이페이지 | 서비스장바구니 |  | CLICK |
| 29 | ALL | service_giftcard | 서비스_쿠폰함 | 마이페이지 | 서비스쿠폰함 |  | CLICK |
| 147 | MO | mypage_agreement | 마이페이지_설정 > 마케팅 수신동의 | 마이페이지 | 설정 | 마케팅 수신동의 | CLICK |
| 15 | ALL | mypage_reservation_list | 마이페이지_예약내역 | 마이페이지 | 예약내역 |  | CLICK |
| 216 | MO | mypage_reservation_OvrsAir | 마이페이지>예약내역_해외항공 | 마이페이지 | 예약내역_해외항공 |  | CLICK |
| 23 | ALL | mypage_event | 마이페이지_이벤트참여내역 | 마이페이지 | 이벤트참여 |  | CLICK |
| 21 | ALL | mypage_faq | 마이페이지_자주찾는질문 | 마이페이지 | 자주찾는질문 |  | CLICK |
| 88 | ALL | shopping_cart_delete_pkg_tgt | 찜 _ 담기 삭제(패키지) | 마이페이지 | 찜_패키지 | 찜 삭제 | CLICK |
| 90 | ALL | shopping_cart_delete_pkg_pre | 장바구니(찜) 삭제(패키지)_자동 발생 | 마이페이지 | 찜_패키지 | 찜 삭제 | CLICK |
| 92 | ALL | shopping_cart_delete_pkg_all | 장바구니(찜) 전체 삭제_패키지 | 마이페이지 | 찜_패키지 | 찜 전체삭제 | CLICK |
| 86 | ALL | shopping_cart_rcmn_pkg | 찜 _ 상품추천 클릭(패키지) | 마이페이지 | 찜_패키지 | 찜_추천상품 | CLICK |
| 89 | ALL | shopping_cart_delete_hotel_tgt | 찜 _ 담기 삭제(호텔) | 마이페이지 | 찜_호텔 | 찜 삭제 | CLICK |
| 91 | ALL | shopping_cart_delete_hotel_pre | 장바구니(찜) 삭제(호텔)_자동 발생 | 마이페이지 | 찜_호텔 | 찜 삭제 | CLICK |
| 93 | ALL | shopping_cart_delete_hotel_all | 장바구니(찜) 전체 삭제_호텔 | 마이페이지 | 찜_호텔 | 찜 전체삭제 | CLICK |
| 87 | ALL | shopping_cart_rcmn_hotel | 찜 _ 상품추천 클릭(호텔) | 마이페이지 | 찜_호텔 | 찜_추천상품 | CLICK |
| 16 | ALL | mypage_shopping_cart | 마이페이지_장바구니(찜) | 마이페이지 | 찜목록 |  | CLICK |
| 19 | ALL | mypage_coupon | 마이페이지_쿠폰함 | 마이페이지 | 쿠폰함 |  | CLICK |
| 151 | MO | mypage_reservation_fnd | 마이페이지 투어/입장권 | 마이페이지 | 투어/입장권 |  | CLICK |
| 153 | MO | mypage_reservation_pkg | 마이페이지 패키지 | 마이페이지 | 패키지 |  | CLICK |
| 152 | MO | mypage_reservation_hotel | 마이페이지 호텔 | 마이페이지 | 호텔 |  | CLICK |

---

## 마이메뉴·예약내역 (15건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 133 | PC | mymenu | 마이메뉴 | 마이메뉴 |  |  | CLICK |
| 13 | ALL | mymenu_oneonone | 마이메뉴_1:1상담 | 마이메뉴 | 1:1상담 |  | CLICK |
| 12 | ALL | mymenu_q&a | 마이메뉴_참여내역 | 마이메뉴 | Q&A |  | CLICK |
| 14 | ALL | mymenu_privacy | 마이메뉴_개인정보수정 | 마이메뉴 | 개인정보수정 |  | CLICK |
| 11 | ALL | mymenu_mypage | 마이메뉴_마이페이지 | 마이메뉴 | 마이페이지 |  | CLICK |
| 10 | ALL | mymenu_mileage | 마이메뉴_마일리지 | 마이메뉴 | 마일리지 |  | CLICK |
| 7 | ALL | mymenu_reservation_list | 마이메뉴_예약내역 | 마이메뉴 | 예약내역 |  | CLICK |
| 8 | ALL | mymenu_shopping_cart | 마이메뉴_장바구니(찜) | 마이메뉴 | 찜목록 |  | CLICK |
| 9 | ALL | mymenu_coupon | 마이메뉴_쿠폰 | 마이메뉴 | 쿠폰 |  | CLICK |
| 60 | ALL | reservation_cancel_pkg | 패키지예약 취소완료 | 마이메뉴 | 패키지 예약내역 | 취소 | LOAD |
| 62 | ALL | reservation_cancel_air | 항공예약 취소완료 | 마이메뉴 | 항공 예약내역 | 취소 | LOAD |
| 61 | ALL | reservation_cancel_hotel | 호텔예약 취소완료 | 마이메뉴 | 호텔 예약내역 | 취소 | LOAD |
| 134 | PC | reservation_list | 예약내역 | 예약내역 |  |  | CLICK |
| 79 | ALL | reservation_cancel_air_rcmn | 항공취소시 추천 상품 | 예약내역 | 항공취소내역 | 취소 상품추천 | CLICK |
| 80 | ALL | reservation_cancel_htl_rcmn | 호텔 취소시 추천 상품 | 예약내역 | 호텔취소내역 | 취소 상품추천 | CLICK |

---

## 로그인·회원가입 (18건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 4 | ALL | log_out / logout | 로그아웃 | 로그아웃 |  |  | CLICK |
| 1 | ALL | log_in_button | 로그인(버튼 클릭) | 로그인 |  |  | CLICK |
| 3 | ALL | log_in | 로그인 | 로그인 | 로그인(버튼) |  | CLICK |
| 6 | ALL | log_in_result | 로그인 결과 | 로그인 | 로그인(버튼) |  | LOAD |
| 156 | ALL | password_finding | 비밀번호 찾기 | 로그인 | 비밀번호 찾기 |  | CLICK |
| 157 | ALL | password_finding_certify | 비밀번호 찾기_본인인증 | 로그인 | 비밀번호 찾기 |  | CLICK |
| 158 | ALL | password_reset | 비밀번호 찾기_비밀번호 변경 | 로그인 | 비밀번호 찾기 | 비밀번호 재설정 | CLICK |
| 159 | ALL | password_reset_cancel | 비밀번호 찾기_비밀번호 취소 | 로그인 | 비밀번호 찾기 | 비밀번호 재설정 | CLICK |
| 2 | ALL | log_in_non_account | 비회원 예약조회 | 로그인 | 비회원 예약조회 |  | CLICK |
| 5 | ALL | log_in_non_reservation | 비회원 예약하기 클릭 | 로그인 | 비회원 예약하기 |  | CLICK |
| 136 | ALL | id_finding | 아이디 찾기 | 로그인 | 아이디 찾기 |  | CLICK |
| 137 | ALL | id_finding_certify | 아이디 찾기_본인인증 | 로그인 | 아이디 찾기 |  | CLICK |
| 195 | ALL | unify_member_joinning_start | 통합 회원가입_시작 | 회원가입 | 통합 회원가입(버튼) |  | CLICK |
| 190 | ALL | unify_member_joinning_agree | 통합 회원가입_약관동의 | 회원가입 | 통합 회원가입(버튼) | 약관동의 | CLICK |
| 191 | ALL | unify_member_joinning_certify | 통합 회원가입_본인인증 | 회원가입 | 통합 회원가입(버튼) | 약관동의 | CLICK |
| 192 | ALL | unify_member_joinning_complete | 통합 회원가입_완료 | 회원가입 | 통합 회원가입(버튼) | 약관동의 | LOAD |
| 193 | ALL | unify_member_joinning_complete_banner | 통합 회원가입_완료_배너 | 회원가입 | 통합 회원가입(버튼) | 약관동의 | CLICK |
| 194 | ALL | unify_member_joinning_personal_info | 통합 회원가입_정보입력 | 회원가입 | 통합 회원가입(버튼) | 약관동의 | CLICK |

---

## 플레이스 (10건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 125 | MO | main_place | 메인_플레이스 | 플레이스 |  |  | CLICK |
| 160 | MO | place_group_city | 플레이스_그룹지역_단일지역 | 플레이스 | 그룹지역 | 단일지역 | CLICK |
| 162 | MO | place_landmark | 플레이스_랜드마크 | 플레이스 | 단일지역 | 랜드마크 | CLICK |
| 163 | MO | place_menu_shortcut | 플레이스_퀵메뉴 | 플레이스 | 단일지역 | 메뉴숏컷 | CLICK |
| 165 | MO | place_rcmn | 플레이스_추천상품 | 플레이스 | 단일지역 | 추천상품 | CLICK |
| 166 | MO | place_theme | 플레이스_테마여행 | 플레이스 | 단일지역 | 테마여행 | CLICK |
| 164 | MO | place_planner | 플레이스_추천일정 | 플레이스 | 단일지역 | 플래너 | CLICK |
| 126 | MO | main_place_list | 플레이스 > 전체도시 > 도시클릭 | 플레이스 | 전체도시 | 도시 클릭 | CLICK |
| 144 | MO | load_place | 플레이스 로딩 | 플레이스 | 플레이스 클릭 | 플레이스 페이지 | LOAD |
| 161 | MO | place_home_menu | 플레이스_홈메뉴 | 플레이스 | 홈메뉴 |  | CLICK |

---

## 플래너 (18건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 154 | MO | myplanner_myplan_list | 플래너_MY플래너_나의여행일정목록 | 플래너 | MY플래너 | MY플랜 | CLICK |
| 155 | MO | myplanner_rcmn_pkg | 플래너_MY플래너_추천상품 | 플래너 | MY플래너 | 추천상품 | CLICK |
| 169 | MO | planner_myplan_list | 플래너_MY여행일정 | 플래너 | MY플랜 |  | CLICK |
| 174 | MO | planner_plan_start | 플래너_MY플랜_생성 | 플래너 | MY플랜 | 생성 | CLICK |
| 171 | MO | planner_plan_edit | 플래너_MY플랜_일정수정 | 플래너 | MY플랜 | 설정변경 | CLICK |
| 168 | MO | planner_list_by_city | 플래너_관심도시_추천일정목록 | 플래너 | 관심도시 | 플랜리스트 | CLICK |
| 120 | MO | load_planner | 플래너 > 내 여행일정 클릭 | 플래너 | 내 여행일정 | 내 여행 페이지 | LOAD |
| 167 | MO | planner_banner | 플래너_배너 | 플래너 | 배너 |  | CLICK |
| 209 | MO | load_planner_pageBack | 플래너_새일정만들기_뒤로가기 | 플래너 | 새일정만들기(버튼) | 뒤로가기(버튼) | CLICK |
| 176 | MO | planner_rcmn_manager | 플래너_관리자등록 추천일정 | 플래너 | 최하단 추천플랜 |  | CLICK |
| 210 | MO | load_rcmn_planner | 플래너_추천 플래너 | 플래너 | 추천 플래너 |  | CLICK |
| 211 | MO | load_rcmn_planner_pageBack | 플래너_추천 플래너_뒤로가기 | 플래너 | 추천 플래너 | 뒤로가기(버튼) | CLICK |
| 175 | MO | planner_rcmn_city | 플래너_추천도시 | 플래너 | 추천도시 |  | CLICK |
| 177 | MO | planner_rcmn_pkg | 플래너_추천상품(패키지) | 플래너 | 추천상품 |  | CLICK |
| 178 | MO | planner_rcmn_planner | 플래너_추천스케줄(인기순/최신순) | 플래너 | 추천플랜 |  | CLICK |
| 173 | MO | planner_plan_share | 플래너_플랜_일정공유 | 플래너 | 플랜 | 공유 | CLICK |
| 170 | MO | planner_plan_copy | 플래너_내일정으로담기 | 플래너 | 플랜 | 담기 | CLICK |
| 172 | MO | planner_plan_repl | 플래너_플랜_일정댓글달기 | 플래너 | 플랜 | 댓글 | CLICK |

---

## 기획전·이벤트 (15건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 45 | ALL | load_exhibition | 페이지 로드_기획전 | 기획전 | 기획전 상세 |  | LOAD |
| 105 | ALL | coupon_download | 쿠폰 다운로드 | 기획전 | 쿠폰다운로드 |  | CLICK |
| 132 | PC | mdpage | 여행기획전 | 여행기획전 |  |  | CLICK |
| 221 | ALL | scroll_exhibition_100% | 기획전 스크롤 100% | 여행기획전 | 기획전 상세 | 기획전 상세 100% |  |
| 222 | ALL | scroll_exhibition_25% | 기획전 스크롤 25% | 여행기획전 | 기획전 상세 | 기획전 상세 25% |  |
| 223 | ALL | scroll_exhibition_50% | 기획전 스크롤 50% | 여행기획전 | 기획전 상세 | 기획전 상세 50% |  |
| 224 | ALL | scroll_exhibition_75% | 기획전 스크롤 75% | 여행기획전 | 기획전 상세 | 기획전 상세 75% |  |
| 201 | ALL | exhibition_banner | 기획전 배너 | 여행기획전 | 기획전 상세 | 배너 | CLICK |
| 205 | ALL | exhibition_md | 기획전 수동상품 | 여행기획전 | 기획전 상세 | 상품 | CLICK |
| 204 | ALL | exhibition_img | 기획전 이미지 | 여행기획전 | 기획전 상세 | 이미지 | CLICK |
| 203 | ALL | exhibition_coupon | 기획전 쿠폰 | 여행기획전 | 기획전 상세 | 쿠폰 | CLICK |
| 200 | ALL | exhibition_air_auto_md | 기획전 항공 자동상품 | 여행기획전 | 기획전 상세 | 항공 자동상품 | CLICK |
| 202 | ALL | exhibition_benefit | 기획전 혜택 | 여행기획전 | 기획전 상세 | 혜택 포함 상품 | CLICK |
| 116 | ALL | load_event | 페이지로드 _ 이벤트영역 | 이벤트 | 기획전 |  | LOAD |
| 115 | ALL | apct_event | 이벤트참여 | 이벤트 | 기획전 | 응모하기 | CLICK |

---

## 제우스 (5건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 97 | ALL | smn_zeus_md | 서브홈_제우스 > MD상품추천 | 제우스 | MD추천 |  | CLICK |
| 96 | ALL | smn_zeus_mdpage | 서브홈_제우스 > 기획전 | 제우스 | 기획전 |  | CLICK |
| 95 | ALL | smn_zeus_menu | 서브홈_제우스 > 메뉴 | 제우스 | 메뉴 |  | CLICK |
| 98 | ALL | smn_zeus_banner | 서브홈_제우스 > 배너 | 제우스 | 배너 |  | CLICK |
| 94 | ALL | smn_zeus_home | 서브홈_제우스 | 제우스 | 홈 |  | CLICK |

---

## 하나LIVE (7건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 122 | MO | main_live | 메인_하나LIVE | 하나LIVE |  |  | CLICK |
| 141 | MO | live_preview | 하나LIVE 방송예정 | 하나LIVE | 라이브 미리보기 |  | CLICK |
| 142 | MO | live_prod | 하나LIVE 대표방송 | 하나LIVE | 라이브 예정상품 |  | CLICK |
| 140 | MO | live_list | 하나LIVE 지난방송 | 하나LIVE | 지난 방송 |  | CLICK |
| 123 | MO | main_live_list | 메인_하나LIVE > 전체방송보기 | 하나LIVE 전체방송보기 |  |  | CLICK |
| 208 | MO | live_prod_pre | 하나라이브_쿠폰_뒤로가기 | 하나라이브 | 라이브 쿠폰 | 뒤로가기 | CLICK |
| 207 | MO | live_list_pre | 하나라이브 지난방송_뒤로가기 | 하나라이브 | 지난방송 | 뒤로가기 | CLICK |

---

## 메인·검색 (23건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 38 | ALL | main_md | 메인 _ MD추천영역 클릭 | MD추천영역 |  |  | CLICK |
| 42 | ALL | main_popup_mkt | 메인 팝업(마케팅) | popup |  |  | CLICK |
| 35 | ALL | main_rcmn | 메인 추천상품영역 클릭 | 검색추천 |  |  | CLICK |
| 124 | MO | main_magazine | 메인_매거진 | 매거진 | 매거진 |  | CLICK |
| 215 | PC | main_video_banner | 메인_동영상+배너 | 메인 | 동영상+배너 |  | CLICK |
| 214 | PC | main_slide_banner | 메인_배너 | 메인 | 슬라이드 배너 |  | CLICK |
| 197 | MO | appInstall_banner | 메인_앱설치 배너 | 메인 | 앱설치 배너 |  | CLICK |
| 213 | MO | main_openchat | 메인_오픈챗 | 메인 | 오픈챗 |  | CLICK |
| 212 | PC | main_major_service | 메인_주요서비스 | 메인 | 주요서비스 |  | CLICK |
| 206 | MO | keyword_exhibition_tile | 키워드 기획전 타일 | 메인 | 키워드 기획전 타일 |  | CLICK |
| 145 | MO | main_planner | 메인_플래너 | 메인 | 플래너 |  | CLICK |
| 36 | ALL | main_top | 메인 top롤링배너 클릭 | 메인 배너 |  |  | CLICK |
| 41 | ALL | main_menu | 메인 메뉴 클릭(GNB) | 메인메뉴 |  |  | CLICK |
| 43 | ALL | main_home | 메인 홈버튼 | 메인홈 |  |  | CLICK |
| 121 | MO | main_event_banner | 메인_이벤트배너 | 이벤트배너 |  |  | CLICK |
| 40 | ALL | main_popular | 메인 _ 추천/인기여행지영역 | 인기여행지 영역 |  |  | CLICK |
| 32 | ALL | main_search_pkg | 퀵서치_패키지검색 | 퀵서치 패키지 |  |  | CLICK |
| 33 | ALL | main_search_air | 퀵서치_항공권검색 | 퀵서치 항공권 |  |  | CLICK |
| 34 | ALL | main_search_hotel | 퀵서치_호텔검색 | 퀵서치 호텔 |  |  | CLICK |
| 44 | ALL | hotdeal | 핫딜영역_타임세일 | 타임세일 |  |  | CLICK |
| 37 | ALL | main_tabarea | 탭형 상품영역 클릭 | 탭형 상품영역 |  |  | CLICK |
| 39 | ALL | main_theme | 메인 _ 테마여행추천상품영역 | 테마영역 |  |  | CLICK |
| 31 | ALL | search | 통합검색 | 통합검색 |  |  | CLICK |

---

## 기타 (18건)

| 순번 | PC/MO | Event Name (EN) | Event Name (KR) | 1 Depth | 2 Depth | 3 Depth | 호출시점 |
|--|--|--|--|--|--|--|--|
| 180 | MO | session_end |  |  |  |  |  |
| 181 | MO | session_start |  |  |  |  |  |
| 198 | ALL | clicked_detail_pkg_rcmn_fnd | 결합상품_추천FND상품 상세보기 | 결합 상품 | 추천 FND 상품 |  | CLICK |
| 188 | ALL | smn_slide_banner | 모든 서브페이지 하단 배너 | 모든 서브페이지 | 하단 배너 |  | CLICK |
| 228 | PC | smn_pkg_sns | 서브홈_패키지>밴드+플친마케팅 | 서브홈 | 밴드+플친마케팅 |  | CLICK |
| 227 | PC | smn_horizon_banner | 서브홈_패키지>배너 | 서브홈 | 슬라이드 배너 |  | CLICK |
| 229 | PC | smn_pkg_tabarea | 서브홈_패키지>키워드상품목록 | 서브홈 | 슬라이드 키워드상품목록 |  | CLICK |
| 225 | MO | short_all | 숏플_전체보기_숏츠영상 | 숏플 | 전체보기(텍스트) | 숏츠영상 | CLICK |
| 217 | MO | player_product | 숏플영상 연관상품 | 숏플 | 전체보기(텍스트) | 숏츠영상>상품 | CLICK |
| 226 | MO | short_filter | 숏츠_전체보기_필터 | 숏플 | 전체보기(텍스트) | 필터 | CLICK |
| 138 | MO | init_app_mkt_yn | (앱 최초 실행) 마케팅 동의여부 | 앱 최초 실행 |  |  | CLICK |
| 139 | MO | init_app_push_yn | (앱 최초 실행) 앱푸시 수신 동의여부 | 앱 최초 실행 |  |  | CLICK |
| 81 | ALL | shopping_cart | 장바구니(찜) | 장바구니(찜) |  |  | CLICK |
| 189 | MO | smn_thumb_banner | 제주/국내_썸네일 배너 | 제주/국내 | 썸네일 배너 |  | CLICK |
| 183 | PC | shoping_cart_delete_pkg_all | 장바구니(찜) 전체 삭제_패키지 | 찜 | 패키지 | 전체삭제 | LOAD |
| 182 | PC | shoping_cart_delete_hotel_all | 장바구니(찜) 전체 삭제_호텔 | 찜 | 호텔/펜션 | 전체삭제 | LOAD |
| 179 | MO | rcnt_prod_list | 최근 본/찜_최근 본 | 최근 본/찜 |  |  | CLICK |
| 143 | ALL | load_pages | 페이지로드(기본) | 페이지로드(기본) |  |  | LOAD |

---

## 변경 이력

| 날짜 | 내용 | 작성자 |
|--|--|--|
| 2026.03.25 | 초안 생성 (229개 이벤트, Navigation별 그룹화) | - |
| 2026.03.25 | 1Depth 기준 그룹화로 재편, Navigation 컬럼 제거 | - |
