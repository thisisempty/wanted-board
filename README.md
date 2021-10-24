# 게시판 CRUD 

## 적용 기술
* python==3.8.12
* django==3.2.8
* PyJWT==2.3.0
* bcrypt==3.2.0

## Endpoint
- 회원가입 : `/users/signup`
- 로그인 : `/users/signin`
- 게시물 작성 : `/posts/register`
- 게시물 수정 : `/posts/<int:post_id>`
- 게시물 삭제 : `/posts/<int:post_id>`
- 게시물 로드 : `/posts?limit=30&offset=0` 
- 게시물 확인 : `/posts/detail?id=<int:post_id>`

-----

# Users
## 회원가입
- bcrypt를 사용하여 회원 정보 암호화 하여 저장

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/users/signup`|(JSON) account_id, password | (JSON) 에러 / 성공 메시지 |

### request 예시
``` json 
{
	"account_id" : "sampleid1234",
	"password" : "Qwerty123!"
}
```
- account_id : 유저가 사용할 id
- password : 유저가 사용할 password
  
### response 예시
``` json
// 성공 시
{
    "message": "SUCCESS"
}

// 실패 시 
// 필요한 값이 누락 되었을 시
{ 
    "message" : "KEY_ERROR"
}

// 존재하는 id 사용 시
{ 
    "message" : "ALREADY_EXIST"
}

// 비밀번호 정규화 식에 맞지 않을 시
// 8자리 이상, 특수문자, 소문자, 대문자 포함
{
    "message" : "INVAILD_PASSWORD"
}

// 아이디 정규화 식에 맞지 않을 시
// 소문자, 숫자, -_. 만 사용 가능
{
    "message" : "INVAILD_ID"
}
```

## 로그인
- 로그인 성공 시 JWT를 사용한 ACCESS_TOKEN 전달

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`GET`|`/users/signin`|(JSON) account_id, password | (JSON)ACCESS_TOKEN / 에러 메시지 |

- account_id : 유저가 사용하는 id
- password : 유저가 사용하는 password

### request 예시
``` json 
{
	"account_id" : "sampleid1234",
	"password" : "Qwerty123!"
}
```

### response 예시
``` json 
// 성공시
{
  "ACCESS_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NX0.kjySYfRP9DYViWyNPW0YGchAs6p5bnstirSN5P91yMM"
}

// 실패시
// 패스워드 틀릴 경우
{
    "message" : "INVALID_PASSWORD"
}
// 필요한 값 누락 시
{ 
    "message" : "KEY_ERROR"
}

// 존자하지 않는 아이디 사용 시
{ 
    "message" : "DOES_NOT_EXIST"
}
```

-----

# Posts
## 게시물 작성
- 가입된 유저만 게시물을 작성할 수 있다.
- 게시물의 제목과 내용을 작성해야 한다.

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/posts/register`|(JSON) access_token, title, body  | (JSON) 에러 / 성공 메시지 |

- access_token : 유저 로그인 시 발행된 access_token
- title : 게시물 제목
- body : 게시물 내용

### request 예시
``` json 
headers : {
    "Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NX0.kjySYfRP9DYViWyNPW0YGchAs6p5bnstirSN5P91yMM"
}
body : {
	"title" : "게시물 제목",
	"body"  : "게시물 내용"
}
```
### response 예시
``` json
// 성공 시
{
    "message": "SUCCESS"
}

// 실패 시 
// 필요한 값 누락 시
{ 
    "message" : "KEY_ERROR"
}
```

## 게시물 수정
- 작성자만 게시물을 삭제할 수 있다
- 제목만 수정하거나 내용만 수정 할 수도 있고 둘 다 수정할 수 있다.

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/posts/<int:post_id>`|(JSON) access_token, title, body  | (JSON) 에러 / 성공 메시지 |
- access_token : 유저 로그인 시 발행된 access_token
- title : 수정할 게시물 제목
- body : 수정할 게시물 내용

### request 예시
``` json 
headers : {
    "Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NX0.kjySYfRP9DYViWyNPW0YGchAs6p5bnstirSN5P91yMM"
}
body : {
	"title" : "수정한 게시물 제목",
}
```

### response 예시
``` json
// 성공 시
{
    "message": "SUCCESS"
}

// 실패 시 
// 존재하지 않는 게시물을 수정 요청 할 시 
{ 
    "message" : "DOES_NOT_EXIST"
}
```

## 게시물 삭제
- 작성자만 게시물을 삭제할 수 있다.
  
|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/posts/<int:post_id>`|(JSON) access_token | (JSON) 에러 / 성공 메시지 |
- access_token : 유저 로그인 시 발행된 access_token

### request 예시
``` json 
headers : {
    "Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NX0.kjySYfRP9DYViWyNPW0YGchAs6p5bnstirSN5P91yMM"
}
```

### response 예시
``` json
// 성공 시
{
    "message": "SUCCESS"
}

// 실패 시 
// 존재하지 않는 게시물을 삭제 요청 할 시 
{ 
    "message" : "DOES_NOT_EXIST"
}
```

## 게시물 확인
- 모든 유저는 게시물을 확인할 수 있다.

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/posts/detail?id=<int:post_id>`| None | (JSON) 게시물 정보 / 에러 메시지 |

### response 예시
``` json
// 성공 시
{
  "user_id": "sampleid1234",
  "title": "게시물 제목",
  "body": "게시물 내용",
  "created_at": "2021-10-24T08:23:16.673Z"
}

// 실패 시 
// 존재하지 않는 게시물 정보를 요청 할 시 
{ 
    "message" : "DOES_NOT_EXIST"
}
```

## 게시물 로드
- offset 값 부터 limit값 까지의 개수만큼 전달한다.
- 모든 유저가 접근할 수 있다.

|METHOD|PATH|request|response|
|:--:|:--:|:--:|:--:|
|`POST`|`/posts?limit=5&offset=0| None | (JSON) 게시물 정보 / 에러 메시지|

### response 예시
``` json
// 성공 시
{
  "count": 5,
  "data": [
    {
      "post_id": 1,
      "user_id": "sampleid1234",
      "title": "수정한 게시물 제목3",
      "created_at": "2021-10-24T07:17:29.545Z"
    },
    {
      "post_id": 2,
      "user_id": "sampleid1234",
      "title": "두 번째 게시물",
      "created_at": "2021-10-24T07:21:05.000Z"
    },
    {
      "post_id": 3,
      "user_id": "sampleid1234",
      "title": "1",
      "created_at": "2021-10-24T08:21:47.634Z"
    },
    {
      "post_id": 4,
      "user_id": "sampleid1234",
      "title": "1",
      "created_at": "2021-10-24T08:23:16.673Z"
    },
    {
      "post_id": 5,
      "user_id": "sampleid1234",
      "title": "1",
      "created_at": "2021-10-24T08:23:16.870Z"
    }
  ]
}

// 실패 시 
// 잘못된 값으로 요청 시  
{ 
    "message" : "VALUE_ERROR"
}