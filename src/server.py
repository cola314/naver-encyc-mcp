import sys
import argparse
import asyncio
from typing import Dict, Any
from fastmcp import FastMCP
from naver_api import NaverAPIClient, NaverAPIError
from models import EncyclopediaSearchRequest, EncyclopediaSearchResponse, EncyclopediaItem, ErrorResponse
from config.settings import settings

class NaverEncyclopediaMCPServer:
    def __init__(self):
        self.api_client = NaverAPIClient()
        self.mcp = FastMCP()
        self._register_functions()
    
    def _register_functions(self):
        """MCP 함수 등록"""
        @self.mcp.tool(
            name="search_encyclopedia",
            description="네이버 백과사전에서 검색어로 관련 정보를 검색합니다."
        )
        def search_encyclopedia(query: str, display: int = 10, start: int = 1) -> Dict[str, Any]:
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
                error_response = ErrorResponse(
                    error_code=e.error_code,
                    message=e.message,
                    status_code=e.status_code
                )
                return error_response.dict()
            except Exception as e:
                error_response = ErrorResponse(
                    error_code="UNKNOWN_ERROR",
                    message=f"예상치 못한 오류: {str(e)}",
                    status_code=500
                )
                return error_response.dict()
    
    def run_stdin_stdout(self):
        """stdin/stdout 모드로 서버 실행"""
        asyncio.run(self.mcp.run_stdio_async())
    
    def run_http(self, host: str = "localhost", port: int = 8000):
        """HTTP 모드로 서버 실행"""
        asyncio.run(self.mcp.run_http_async(host=host, port=port))

def main():
    parser = argparse.ArgumentParser(description="네이버 백과사전 검색 MCP 서버")
    parser.add_argument(
        "--mode",
        choices=["stdin", "http"],
        default="stdin",
        help="서버 실행 모드 (기본값: stdin)"
    )
    parser.add_argument(
        "--host",
        default=settings.MCP_SERVER_HOST,
        help=f"HTTP 서버 호스트 (기본값: {settings.MCP_SERVER_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.MCP_SERVER_PORT,
        help=f"HTTP 서버 포트 (기본값: {settings.MCP_SERVER_PORT})"
    )
    
    args = parser.parse_args()
    
    server = NaverEncyclopediaMCPServer()
    
    if args.mode == "stdin":
        print("네이버 백과사전 검색 MCP 서버를 stdin/stdout 모드로 실행합니다.", file=sys.stderr)
        server.run_stdin_stdout()
    else:
        print(f"네이버 백과사전 검색 MCP 서버를 HTTP 모드로 실행합니다. (http://{args.host}:{args.port})", file=sys.stderr)
        server.run_http(args.host, args.port)

if __name__ == "__main__":
    main() 