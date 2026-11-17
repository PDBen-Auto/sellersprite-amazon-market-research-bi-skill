# SellerSprite 시장 조사와 BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

사용자가 명시한 출력 언어를 따르고, 지정이 없으면 요청 언어를 따릅니다. 명령, 스킬 ID, JSON 키, 열거값, 단위와 원문 인용은 유지합니다. 번역과 원문을 구분하고 언어로 국가, 통화, 관할을 추정하지 않습니다. 전체 명세의 관련 자료를 읽고 기존 검증과 권한 조건을 적용합니다.

## 설치와 사용

저장소를 내려받거나 복제한 뒤 아래 스킬 디렉터리를 기존 references, scripts, assets 등과 함께 호스트의 스킬 디렉터리에 복사합니다. 이름과 SKILL.md는 유지합니다. 문서 언어만 바꾸는 경우 재설치할 필요가 없습니다. 설치 명령은 선택지이며 설치 또는 활성화 완료를 뜻하지 않습니다.

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## SellerSprite 시장 조사와 BI

`sellersprite-bi-market-research`

시드 의도에서 관련 ASIN을 확장하고 시장층을 구분하여 상위 ASIN 기준 중복 제거 BI를 만듭니다.

스킬 디렉터리: `.`

**구현 근거와 의존성**

명확한 시장/과제·표준/상세 XLSX·필요 키워드 표, Python 3와 openpyxl. 온라인은 승인 SellerSprite 계정/브라우저가 필요하며 추정은 Amazon 정산 자료가 아닙니다.

**입력**

범위/날짜/시장/포함·제외 기준, 탐색용 seed_keyword/seed_asins. 조건부 키워드·표준·상세 내보내기, 선택 관련성·속성·출력 위치. 자격 증명은 금지합니다.

**출력**

이유·상세 범위가 있는 후보 manifest, 상위/월/연/YTD/동기간/브랜드 매출/순위 모멘텀, 자체 포함 dashboard.html, 감사·결측 기록.

[실행 절차 · 제약과 중단 조건 · 요청 예시](references/i18n/ko.md)

> 다음 스킬을 사용하세요: `$sellersprite-bi-market-research` — 키워드·경쟁 표에서 직접 시장 대시보드를 만들고 상세 미포함 후보를 매출 분모에 넣지 않습니다. 한국어로 답하고 근거, 미확인 사항과 작업 권한을 유지하세요.

## 언어 지원과 검증

이 문서는 목적, 전제, 입출력, 절차, 예시와 제약을 다루는 한국어 운영 가이드이며 모든 참고 문서의 문장별 번역은 아닙니다. 상세 기술 자료, 과거 사례, 스크립트 오류, 예제 화면과 이미지는 원래 언어를 유지합니다. 요청 시 해당 언어로 설명할 수 있습니다. 구조, 링크와 핵심 제약을 확인했으나 각 언어 원어민 교정은 수행하지 않았습니다.

전달 전에 입력, 근거, 결측값, 출력 파일과 원래 완료 기준을 대조합니다. 실행하지 않은 단계는 미검증으로 표시하며 스크립트의 정상 종료를 업무 검증 성공으로 취급하지 않습니다.
