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