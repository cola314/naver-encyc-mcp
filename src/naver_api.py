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
        if not settings.NAVER_CLIENT_ID or not settings.NAVER_CLIENT_SECRET:
            raise NaverAPIError("CONFIG_ERROR", "네이버 API 키가 설정되지 않았습니다.", 500)
        
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