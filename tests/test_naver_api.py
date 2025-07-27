import unittest
from unittest.mock import patch, Mock
import sys
import os
import requests

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.naver_api import NaverAPIClient, NaverAPIError

class TestNaverAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = NaverAPIClient()
    
    @patch('src.naver_api.settings')
    @patch('requests.get')
    def test_search_encyclopedia_success(self, mock_get, mock_settings):
        # API 키 설정 모킹
        mock_settings.NAVER_CLIENT_ID = "test_client_id"
        mock_settings.NAVER_CLIENT_SECRET = "test_client_secret"
        mock_settings.MAX_DISPLAY = 100
        mock_settings.MAX_START = 1000
        
        # 성공 응답 모킹
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
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
        mock_get.return_value = mock_response
        
        # API 호출 테스트
        result = self.client.search_encyclopedia("테스트")
        
        self.assertEqual(result["total"], 100)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["title"], "테스트 제목")
    
    @patch('src.naver_api.settings')
    @patch('requests.get')
    def test_search_encyclopedia_error(self, mock_get, mock_settings):
        # API 키 설정 모킹
        mock_settings.NAVER_CLIENT_ID = "test_client_id"
        mock_settings.NAVER_CLIENT_SECRET = "test_client_secret"
        mock_settings.MAX_DISPLAY = 100
        mock_settings.MAX_START = 1000
        
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
    
    @patch('src.naver_api.settings')
    @patch('requests.get')
    def test_search_encyclopedia_network_error(self, mock_get, mock_settings):
        # API 키 설정 모킹
        mock_settings.NAVER_CLIENT_ID = "test_client_id"
        mock_settings.NAVER_CLIENT_SECRET = "test_client_secret"
        mock_settings.MAX_DISPLAY = 100
        mock_settings.MAX_START = 1000
        
        # 네트워크 오류 모킹
        mock_get.side_effect = requests.RequestException("Connection error")
        
        # 네트워크 오류 처리 테스트
        with self.assertRaises(NaverAPIError) as context:
            self.client.search_encyclopedia("테스트")
        
        self.assertEqual(context.exception.error_code, "NETWORK_ERROR")
        self.assertEqual(context.exception.status_code, 500)

if __name__ == "__main__":
    unittest.main() 