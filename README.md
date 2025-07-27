# 네이버 백과사전 검색 MCP 서버

네이버 백과사전 검색 API를 MCP(Model Context Protocol) 서버로 래핑한 프로젝트입니다.

## 기능

- 네이버 백과사전 검색 API 연동
- stdin/stdout 모드 지원
- HTTP 모드 지원
- 에러 처리 및 로깅
- 테스트 코드 포함

## 설치

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp env.example .env
```

`.env` 파일을 편집하여 네이버 API 키를 설정하세요:

```bash
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
```

## 사용법

### 쉬운 실행 방법 (권장)

```bash
# stdin/stdout 모드 (기본)
python3 run_server.py --mode stdin

# HTTP 모드
python3 run_server.py --mode http --host localhost --port 8000

# 도움말
python3 run_server.py --help
```

### 직접 실행 방법

```bash
# stdin/stdout 모드
PYTHONPATH=. python3 src/server.py --mode stdin

# HTTP 모드
PYTHONPATH=. python3 src/server.py --mode http --host localhost --port 8000

# 도움말
PYTHONPATH=. python3 src/server.py --help
```

## API 키 발급

1. [네이버 개발자 센터](https://developers.naver.com/)에 접속
2. 애플리케이션 등록
3. 검색 API 사용 권한 설정
4. 클라이언트 아이디와 시크릿 발급

## 테스트

```bash
# 모든 테스트 실행
PYTHONPATH=. python3 -m pytest tests/

# 특정 테스트 실행
PYTHONPATH=. python3 -m pytest tests/test_naver_api.py -v
PYTHONPATH=. python3 -m pytest tests/test_server.py -v
```

## 프로젝트 구조

```
naver-encyc-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py          # MCP 서버 메인
│   ├── naver_api.py       # 네이버 API 클라이언트
│   ├── models.py          # 데이터 모델
│   └── config/
│       ├── __init__.py
│       └── settings.py    # 설정 관리
├── tests/
│   ├── __init__.py
│   ├── test_naver_api.py  # API 클라이언트 테스트
│   └── test_server.py     # 서버 테스트
├── docs/                  # 문서
├── requirements.txt       # 의존성
├── env.example           # 환경 변수 예시
├── run_server.py         # 실행 스크립트 (권장)
└── README.md            # 프로젝트 문서
```

## MCP 함수

### search_encyclopedia

네이버 백과사전에서 검색어로 관련 정보를 검색합니다.

**파라미터:**
- `query` (string, 필수): 검색할 키워드
- `display` (integer, 선택): 한 번에 표시할 검색 결과 개수 (기본값: 10, 최대: 100)
- `start` (integer, 선택): 검색 시작 위치 (기본값: 1, 최대: 1000)

**응답:**
```json
{
  "total": 100,
  "start": 1,
  "display": 10,
  "items": [
    {
      "title": "검색 결과 제목",
      "link": "https://example.com",
      "description": "검색 결과 설명",
      "thumbnail": "https://example.com/image.jpg"
    }
  ],
  "last_build_date": "Mon, 26 Sep 2016 10:50:00 +0900"
}
```

## 오류 처리

서버는 다음과 같은 오류 상황을 처리합니다:

- 네이버 API 오류 (SE01, SE02, SE03 등)
- 네트워크 오류
- 설정 오류 (API 키 미설정)
- 예상치 못한 오류

오류 응답 형식:
```json
{
  "error": true,
  "error_code": "ERROR_CODE",
  "message": "오류 메시지",
  "status_code": 400
}
```

## 라이선스

MIT License

## 참고 자료

- [네이버 백과사전 검색 API 문서](https://developers.naver.com/docs/serviceapi/search/encyclopedia/encyclopedia.md)
- [FastMCP 문서](https://github.com/fastmcp/fastmcp)
- [MCP 프로토콜 스펙](https://modelcontextprotocol.io/) 