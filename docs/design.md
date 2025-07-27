# 네이버 백과사전 검색 API MCP 서버 설계 문서

## 1. 프로젝트 개요

**목적**: 네이버 백과사전 검색 API를 MCP(Model Context Protocol) 서버로 래핑하여 AI 모델이 백과사전 정보를 쉽게 검색할 수 있도록 함

**기술 스택**: 
- FastMCP (Python)
- 네이버 검색 API (백과사전 검색)

## 2. API 분석 결과

### 2.1 네이버 백과사전 검색 API 특징
- **엔드포인트**: `https://openapi.naver.com/v1/search/encyc.json`
- **인증 방식**: Client ID + Client Secret (HTTP 헤더)
- **응답 형식**: JSON
- **일일 호출 한도**: 25,000회
- **비로그인 방식 오픈 API**

### 2.2 주요 파라미터
- `query`: 검색어 (필수, UTF-8 인코딩)
- `display`: 한 번에 표시할 결과 개수 (선택, 기본값: 10, 최대: 100)
- `start`: 검색 시작 위치 (선택, 기본값: 1, 최대: 1000)

### 2.3 응답 구조
```json
{
  "lastBuildDate": "검색 결과 생성 시간",
  "total": "총 검색 결과 개수",
  "start": "검색 시작 위치",
  "display": "한 번에 표시할 검색 결과 개수",
  "items": [
    {
      "title": "백과사전 표제어",
      "link": "백과사전 항목 설명 URL",
      "description": "백과사전 항목 설명 요약",
      "thumbnail": "섬네일 이미지 URL"
    }
  ]
}
```

## 3. MCP 서버 설계

### 3.1 핵심 기능 정의

**1. 백과사전 검색 (search_encyclopedia)**
- **설명**: 검색어를 입력받아 네이버 백과사전 검색 결과를 반환
- **입력 파라미터**:
  - `query`: 검색어 (필수)
  - `display`: 결과 개수 (선택, 기본값: 10)
  - `start`: 시작 위치 (선택, 기본값: 1)
- **출력**: 검색 결과 목록 (제목, 링크, 설명, 썸네일)

**2. 백과사전 상세 정보 조회 (get_encyclopedia_detail)**
- **설명**: 특정 백과사전 항목의 상세 정보를 조회
- **입력 파라미터**:
  - `link`: 백과사전 항목 URL
- **출력**: 상세 정보 (HTML 파싱 또는 API 응답)

### 3.2 서버 구조

```
naver-encyc-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py          # FastMCP 서버 메인
│   ├── naver_api.py       # 네이버 API 클라이언트
│   ├── models.py          # 데이터 모델 정의
│   └── utils.py           # 유틸리티 함수
├── config/
│   └── settings.py        # 설정 파일 (API 키 등)
├── tests/
│   └── test_server.py     # 테스트 코드
├── requirements.txt        # 의존성
├── README.md             # 프로젝트 문서
└── .env.example          # 환경 변수 예시
```

### 3.3 데이터 모델

**1. 검색 요청 모델**
```python
class EncyclopediaSearchRequest:
    query: str          # 검색어
    display: int = 10   # 결과 개수
    start: int = 1      # 시작 위치
```

**2. 검색 결과 모델**
```python
class EncyclopediaItem:
    title: str          # 표제어
    link: str           # 링크
    description: str    # 설명
    thumbnail: str      # 썸네일 URL

class EncyclopediaSearchResponse:
    total: int          # 총 결과 수
    start: int          # 시작 위치
    display: int        # 표시 개수
    items: List[EncyclopediaItem]  # 검색 결과 목록
```

## 4. 보안 및 설정 관리

### 4.1 API 키 관리
- **환경 변수 사용**: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`
- **설정 파일**: `config/settings.py`에서 환경 변수 로드
- **보안**: API 키를 코드에 하드코딩하지 않음

### 4.2 에러 처리
- **네이버 API 오류 코드 매핑**
- **HTTP 상태 코드 처리**
- **사용자 친화적 에러 메시지**

## 5. 구현 우선순위

### Phase 1: 기본 기능
1. FastMCP 서버 기본 구조 설정
2. 네이버 API 클라이언트 구현
3. 백과사전 검색 기능 구현
4. 기본 에러 처리

### Phase 2: 고급 기능
1. 상세 정보 조회 기능
2. 검색 결과 필터링
3. 캐싱 기능
4. 로깅 및 모니터링

### Phase 3: 최적화
1. 성능 최적화
2. 테스트 코드 작성
3. 문서화 완료

## 6. 테스트 전략

### 6.1 단위 테스트
- 네이버 API 클라이언트 테스트
- 데이터 모델 검증
- 유틸리티 함수 테스트

### 6.2 통합 테스트
- MCP 서버 엔드포인트 테스트
- 실제 네이버 API 연동 테스트

## 7. 배포 및 운영

### 7.1 개발 환경
- Python 3.8+
- FastMCP 라이브러리
- 환경 변수 설정

### 7.2 운영 고려사항
- **API 호출 한도**: 일일 25,000회 제한 모니터링
- **에러 로깅**: 네이버 API 오류 추적
- **성능 모니터링**: 응답 시간 측정

## 8. 확장성 고려사항

### 8.1 향후 확장 가능한 기능
- 다른 네이버 검색 API 통합 (뉴스, 블로그 등)
- 검색 결과 캐싱
- 검색 히스토리 관리
- 다국어 지원
- 고급 검색 필터링

## 9. 참고 자료

- [네이버 백과사전 검색 API 문서](https://developers.naver.com/docs/serviceapi/search/encyclopedia/encyclopedia.md)
- [FastMCP 문서](https://github.com/fastmcp/fastmcp)
- [MCP 프로토콜 스펙](https://modelcontextprotocol.io/) 