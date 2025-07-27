# 네이버 백과사전 검색 API 참조 문서

## 개요

네이버 백과사전 검색 API는 네이버 검색의 백과사전 검색 결과를 JSON 형식으로 반환하는 RESTful API입니다.

## 기본 정보

- **API 엔드포인트**: `https://openapi.naver.com/v1/search/encyc.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET
- **인증 방식**: Client ID + Client Secret (HTTP 헤더)
- **응답 형식**: JSON
- **일일 호출 한도**: 25,000회

## 요청 파라미터

| 파라미터 | 타입 | 필수 여부 | 설명 | 기본값 | 최대값 |
|---------|------|----------|------|--------|--------|
| query | String | Y | 검색어 (UTF-8 인코딩) | - | - |
| display | Integer | N | 한 번에 표시할 검색 결과 개수 | 10 | 100 |
| start | Integer | N | 검색 시작 위치 | 1 | 1000 |

## HTTP 헤더

API 호출 시 다음 헤더를 포함해야 합니다:

```
X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디}
X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿}
```

## 요청 예시

### cURL 예시
```bash
curl "https://openapi.naver.com/v1/search/encyc.json?query=%EC%A3%BC%EC%8B%9D&display=10&start=1" \
    -H "X-Naver-Client-Id: {YOUR_CLIENT_ID}" \
    -H "X-Naver-Client-Secret: {YOUR_CLIENT_SECRET}"
```

### Python 예시
```python
import requests

url = "https://openapi.naver.com/v1/search/encyc.json"
params = {
    "query": "주식",
    "display": 10,
    "start": 1
}
headers = {
    "X-Naver-Client-Id": "YOUR_CLIENT_ID",
    "X-Naver-Client-Secret": "YOUR_CLIENT_SECRET"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
```

## 응답 구조

### 성공 응답 (200 OK)

```json
{
  "lastBuildDate": "Mon, 26 Sep 2016 10:50:00 +0900",
  "total": 28034,
  "start": 1,
  "display": 10,
  "items": [
    {
      "title": "<b>주식</b>",
      "link": "http://openapi.naver.com/l?AAAB2NPQ+CMBiEf83LSPrxAu3QAQoYYhwZdCNQRSMFaiXh31tMbrjncpdbv8btCioNOYdCH0YUIMtodOauRu8X4DmwOsgbN31i223Gxf08hcRY7/bYjhZ4Pcx9MwAvKUUmmQCW9s+DkUhkB3XePGa3/0ucCk4iryhmKBJMCcFERpPSTXVdX1ty0XijnCzh45zRdcnb07sNux+iWggwrgAAAA==",
      "description": "<b>주식</b>회사의 자본을 이루는 단위로서의 금액 및 이를 전제로 한 주주의 권리·의무(주주권). <b>주식</b>회사는 자본단체이므로 자본이 없이는 성립할 수 없다. 자본은 사원인 주주(株主)의 출자이며, 권리와 의무의...",
      "thumbnail": ""
    }
  ]
}
```

### 응답 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| lastBuildDate | String | 검색 결과 생성 시간 |
| total | Integer | 총 검색 결과 개수 |
| start | Integer | 검색 시작 위치 |
| display | Integer | 한 번에 표시할 검색 결과 개수 |
| items | Array | 검색 결과 배열 |

### items 배열의 각 항목

| 필드 | 타입 | 설명 |
|------|------|------|
| title | String | 백과사전 표제어 (검색어와 일치하는 부분은 `<b>` 태그로 감싸짐) |
| link | String | 백과사전 항목 설명의 URL |
| description | String | 백과사전 항목 설명의 내용을 요약한 패시지 정보 |
| thumbnail | String | 섬네일 이미지 URL |

## 오류 코드

| 오류 코드 | HTTP 상태 코드 | 오류 메시지 | 설명 |
|----------|---------------|------------|------|
| SE01 | 400 | Incorrect query request (잘못된 쿼리요청입니다.) | API 요청 URL의 프로토콜, 파라미터 등에 오류 |
| SE02 | 400 | Invalid display value (부적절한 display 값입니다.) | display 파라미터 값이 허용 범위(1~100)를 벗어남 |
| SE03 | 400 | Invalid start value (부적절한 start 값입니다.) | start 파라미터 값이 허용 범위(1~1000)를 벗어남 |
| SE04 | 400 | Invalid sort value (부적절한 sort 값입니다.) | sort 파라미터 값에 오타 |
| SE06 | 400 | Malformed encoding (잘못된 형식의 인코딩입니다.) | 검색어가 UTF-8로 인코딩되지 않음 |
| SE05 | 404 | Invalid search api (존재하지 않는 검색 api 입니다.) | API 요청 URL에 오타 |
| SE99 | 500 | System Error (시스템 에러) | 서버 내부 오류 |

### 403 오류
개발자 센터에 등록한 애플리케이션에서 검색 API를 사용하도록 설정하지 않았다면 'API 권한 없음'을 의미하는 403 오류가 발생할 수 있습니다.

## 사용 제한

- **일일 호출 한도**: 25,000회
- **display 파라미터**: 최대 100개
- **start 파라미터**: 최대 1000
- **검색어 인코딩**: UTF-8 필수

## 사전 준비 사항

1. 네이버 개발자 센터에서 애플리케이션 등록
2. 클라이언트 아이디와 클라이언트 시크릿 발급
3. 검색 API 사용 권한 설정

## 참고 자료

- [네이버 개발자 센터](https://developers.naver.com/)
- [API 공통 가이드](https://developers.naver.com/docs/common/)
- [개발자 포럼](https://developers.naver.com/forum) 