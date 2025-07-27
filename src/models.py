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

class ErrorResponse(BaseModel):
    error: bool = Field(True, description="오류 발생 여부")
    error_code: str = Field(..., description="오류 코드")
    message: str = Field(..., description="오류 메시지")
    status_code: int = Field(..., description="HTTP 상태 코드") 