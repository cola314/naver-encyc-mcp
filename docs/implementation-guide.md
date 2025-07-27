# 네이버 백과사전 검색 MCP 서버 구현 가이드

## 개요

이 문서는 네이버 백과사전 검색 API를 MCP(Model Context Protocol) 서버로 래핑하는 구현 가이드입니다.

## 사전 요구사항

### 1. 개발 환경
- Python 3.8 이상
- pip (Python 패키지 관리자)
- Git

### 2. 네이버 개발자 계정
- [네이버 개발자 센터](https://developers.naver.com/) 계정
- 애플리케이션 등록 및 API 키 발급

### 3. 필요한 Python 패키지
```bash
pip install fastmcp
pip install requests
pip install python-dotenv
pip install pydantic
```

## 프로젝트 구조 설정

### 1. 디렉토리 구조 생성
```bash
mkdir -p naver-encyc-mcp/src
mkdir -p naver-encyc-mcp/config
mkdir -p naver-encyc-mcp/tests
mkdir -p naver-encyc-mcp/docs
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```bash
# 네이버 API 설정
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here

# 서버 설정
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

## 핵심 컴포넌트 구현

### 1. 설정 관리 (config/settings.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 네이버 API 설정
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
    
    # 네이버 API 엔드포인트
    NAVER_ENCYCLOPEDIA_API_URL = "https://openapi.naver.com/v1/search/encyc.json"
    
    # 서버 설정
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8000))
    
    # API 제한
    MAX_DISPLAY = 100
    MAX_START = 1000
    DAILY_LIMIT = 25000

settings = Settings()
```

### 2. 데이터 모델 (src/models.py)

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class EncyclopediaSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    display: int = Field(default=10, ge=1, le=100, description="결과 개수")
    start: int = Field(default=1, ge=1, le=1000, description="시작 위치")

class EncyclopediaItem(BaseModel):
    title: str = Field(..., description="백과사전 표제어")
    link: str = Field(..., description="백과사전 항목 URL")
    description: str = Field(..., description="백과사전 항목 설명")
    thumbnail: str = Field(default="", description="섬네일 이미지 URL")

class EncyclopediaSearchResponse(BaseModel):
    total: int = Field(..., description="총 검색 결과 개수")
    start: int = Field(..., description="검색 시작 위치")
    display: int = Field(..., description="표시된 결과 개수")
    items: List[EncyclopediaItem] = Field(..., description="검색 결과 목록")
    last_build_date: Optional[str] = Field(None, description="검색 결과 생성 시간")
```

### 3. 네이버 API 클라이언트 (src/naver_api.py)

```python
import requests
from typing import Dict, Any, Optional
from config.settings import settings

class NaverAPIError(Exception):
    """네이버 API 오류를 나타내는 예외 클래스"""
    def __init__(self, error_code: str, message: str, status_code: int):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(f"{error_code}: {message}")

class NaverAPIClient:
    def __init__(self):
        self.base_url = settings.NAVER_ENCYCLOPEDIA_API_URL
        self.headers = {
            "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
        }
    
    def search_encyclopedia(self, query: str, display: int = 10, start: int = 1) -> Dict[str, Any]:
        """
        네이버 백과사전 검색 API 호출
        
        Args:
            query: 검색어
            display: 결과 개수 (1-100)
            start: 시작 위치 (1-1000)
            
        Returns:
            검색 결과 딕셔너리
            
        Raises:
            NaverAPIError: API 호출 실패 시
        """
        params = {
            "query": query,
            "display": min(display, settings.MAX_DISPLAY),
            "start": min(start, settings.MAX_START)
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error_response(response)
                
        except requests.RequestException as e:
            raise NaverAPIError("NETWORK_ERROR", f"네트워크 오류: {str(e)}", 500)
    
    def _handle_error_response(self, response: requests.Response):
        """API 오류 응답 처리"""
        try:
            error_data = response.json()
            error_code = error_data.get("errorCode", "UNKNOWN")
            error_message = error_data.get("errorMessage", "알 수 없는 오류")
        except ValueError:
            error_code = "PARSE_ERROR"
            error_message = "응답 파싱 오류"
        
        raise NaverAPIError(error_code, error_message, response.status_code)
```

### 4. MCP 서버 (src/server.py)

```python
from fastmcp import FastMCP
from typing import Dict, Any
from src.naver_api import NaverAPIClient, NaverAPIError
from src.models import EncyclopediaSearchRequest, EncyclopediaSearchResponse, EncyclopediaItem

class NaverEncyclopediaMCPServer:
    def __init__(self):
        self.api_client = NaverAPIClient()
        self.mcp = FastMCP()
        self._register_functions()
    
    def _register_functions(self):
        """MCP 함수 등록"""
        self.mcp.register_function(
            name="search_encyclopedia",
            description="네이버 백과사전에서 검색어로 관련 정보를 검색합니다.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 키워드"
                    },
                    "display": {
                        "type": "integer",
                        "description": "한 번에 표시할 검색 결과 개수 (기본값: 10, 최대: 100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "start": {
                        "type": "integer",
                        "description": "검색 시작 위치 (기본값: 1, 최대: 1000)",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 1000
                    }
                },
                "required": ["query"]
            },
            handler=self.search_encyclopedia
        )
    
    def search_encyclopedia(self, query: str, display: int = 10, start: int = 1) -> Dict[str, Any]:
        """
        백과사전 검색 함수
        
        Args:
            query: 검색어
            display: 결과 개수
            start: 시작 위치
            
        Returns:
            검색 결과
        """
        try:
            # API 호출
            result = self.api_client.search_encyclopedia(query, display, start)
            
            # 응답 변환
            items = []
            for item in result.get("items", []):
                items.append(EncyclopediaItem(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    description=item.get("description", ""),
                    thumbnail=item.get("thumbnail", "")
                ))
            
            response = EncyclopediaSearchResponse(
                total=result.get("total", 0),
                start=result.get("start", 1),
                display=result.get("display", display),
                items=items,
                last_build_date=result.get("lastBuildDate")
            )
            
            return response.dict()
            
        except NaverAPIError as e:
            return {
                "error": True,
                "error_code": e.error_code,
                "message": e.message,
                "status_code": e.status_code
            }
        except Exception as e:
            return {
                "error": True,
                "error_code": "UNKNOWN_ERROR",
                "message": f"예상치 못한 오류: {str(e)}",
                "status_code": 500
            }
    
    def run(self, host: str = "localhost", port: int = 8000):
        """MCP 서버 실행"""
        self.mcp.run(host=host, port=port)

if __name__ == "__main__":
    server = NaverEncyclopediaMCPServer()
    server.run()
```

## 테스트 구현

### 1. 단위 테스트 (tests/test_naver_api.py)

```python
import unittest
from unittest.mock import patch, Mock
from src.naver_api import NaverAPIClient, NaverAPIError

class TestNaverAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = NaverAPIClient()
    
    @patch('requests.get')
    def test_search_encyclopedia_success(self, mock_get):
        # 성공 응답 모킹
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "total": 100,
            "start": 1,
            "display": 10,
            "items": [
                {
                    "title": "테스트 제목",
                    "link": "http://test.com",
                    "description": "테스트 설명",
                    "thumbnail": ""
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # API 호출 테스트
        result = self.client.search_encyclopedia("테스트")
        
        self.assertEqual(result["total"], 100)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["title"], "테스트 제목")
    
    @patch('requests.get')
    def test_search_encyclopedia_error(self, mock_get):
        # 오류 응답 모킹
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errorCode": "SE01",
            "errorMessage": "잘못된 쿼리요청입니다."
        }
        mock_get.return_value = mock_response
        
        # 오류 처리 테스트
        with self.assertRaises(NaverAPIError) as context:
            self.client.search_encyclopedia("")
        
        self.assertEqual(context.exception.error_code, "SE01")
        self.assertEqual(context.exception.status_code, 400)

if __name__ == "__main__":
    unittest.main()
```

## 실행 방법

### 1. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 실제 API 키 입력
```

### 2. 서버 실행
```bash
# 개발 모드로 실행
python src/server.py

# 또는 FastMCP CLI 사용
fastmcp run src/server.py
```

### 3. 테스트 실행
```bash
# 단위 테스트 실행
python -m pytest tests/

# 특정 테스트 실행
python -m pytest tests/test_naver_api.py -v
```

## 배포 고려사항

### 1. 프로덕션 환경 설정
- 환경 변수 관리 (Docker, Kubernetes 등)
- 로깅 설정
- 모니터링 도구 연동

### 2. 성능 최적화
- API 호출 캐싱
- 연결 풀링
- 비동기 처리

### 3. 보안 고려사항
- API 키 암호화
- 요청 제한 (Rate Limiting)
- 입력 검증 강화

## 문제 해결

### 1. 일반적인 오류
- **403 오류**: API 키가 올바르지 않거나 권한이 없음
- **SE01 오류**: 요청 파라미터가 잘못됨
- **네트워크 오류**: 인터넷 연결 확인

### 2. 디버깅 팁
- 로그 레벨 설정
- API 응답 로깅
- 요청/응답 데이터 검증

## 참고 자료

- [FastMCP 문서](https://github.com/fastmcp/fastmcp)
- [네이버 개발자 센터](https://developers.naver.com/)
- [MCP 프로토콜 스펙](https://modelcontextprotocol.io/) 