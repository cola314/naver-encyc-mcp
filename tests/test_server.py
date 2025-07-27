import unittest
from unittest.mock import patch, Mock
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.server import NaverEncyclopediaMCPServer

class TestNaverEncyclopediaMCPServer(unittest.TestCase):
    def setUp(self):
        # FastMCP 초기화를 모킹하여 테스트 가능하게 만듦
        with patch('src.server.FastMCP') as mock_fastmcp:
            self.mock_mcp = mock_fastmcp.return_value
            self.server = NaverEncyclopediaMCPServer()
    
    def test_server_initialization(self):
        """서버 초기화 테스트"""
        self.assertIsNotNone(self.server)
        self.assertIsNotNone(self.server.api_client)
        self.assertIsNotNone(self.server.mcp)
    
    @patch('src.naver_api.NaverAPIClient.search_encyclopedia')
    def test_api_client_integration(self, mock_search):
        """API 클라이언트 통합 테스트"""
        # 성공 응답 모킹
        mock_search.return_value = {
            "total": 100,
            "start": 1,
            "display": 10,
            "lastBuildDate": "Mon, 26 Sep 2016 10:50:00 +0900",
            "items": [
                {
                    "title": "테스트 제목",
                    "link": "http://test.com",
                    "description": "테스트 설명",
                    "thumbnail": ""
                }
            ]
        }
        
        # API 클라이언트 직접 호출 테스트
        result = self.server.api_client.search_encyclopedia("테스트")
        
        self.assertEqual(result["total"], 100)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["title"], "테스트 제목")
    
    @patch('src.naver_api.NaverAPIClient.search_encyclopedia')
    def test_api_client_error_handling(self, mock_search):
        """API 클라이언트 오류 처리 테스트"""
        # API 오류 모킹
        from src.naver_api import NaverAPIError
        mock_search.side_effect = NaverAPIError("SE01", "잘못된 쿼리요청입니다.", 400)
        
        # 오류 처리 테스트
        with self.assertRaises(NaverAPIError) as context:
            self.server.api_client.search_encyclopedia("")
        
        self.assertEqual(context.exception.error_code, "SE01")
        self.assertEqual(context.exception.status_code, 400)

if __name__ == "__main__":
    unittest.main() 