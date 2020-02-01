# 2019_hanium_project
> https://lab.hanium.or.kr/19-p268/2019_hanium_project
> 
- docker-compose (gunicorn + Django + nginx + mariadb)

### 간단한 동작영상
https://youtu.be/0NGcogvlrlM



## 1. 기능

### 채팅
- channel을 이용하여 통신
- django 권한을 이용하여, 각 방마다 접근 권한 부여

### TTS
- AWS의 boto3를 사용하여, 채팅시 TTS 구현. 
- 현재 계정 연결이 되어있지 않아 해당 이벤트 부분이 비활성화(주석처리) 되어 있다.

### 쇼설로그인
- 로컬에서 로그인 불가

## 2. 파일 및 폴더 설명

#### 2.1 compose folder
- /django: 디장고 도커파일(Dockerfile)
- /nginx: nginx 설정 파일

#### 2.2 hanium folder
- 디장고 프로젝트 패키지

#### 2.3 chat folder
- django chat app: 디장고 채팅 관련 앱

#### 2.4 accounts folder
- django accounts app: 디장고 로그인 관련 앱

#### 2.5 docke-compose.yml
- django
- mariadb
- ngninx

#### 2.6 requirements.txt
- django의 python 패키지 설치 모음

# 도커 설치 및 적용 문서(Ubuntu)
- 적용 운영체제: ubuntu 16.04
1. ```sudo apt update``` //업데이트를 먼저 해쥼
2. ```sudo apt install git``` //깃 사용을 위해 설치
3. ```sudo apt install docker.io``` //도커 설치
4. ```sudo apt install curl```
5. ```sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose``` //docker-compose 1.18버전설치
6. ```sudo chmod +x /usr/local/bin/docker-compose``` //실행파일로 등록

7. ```git clone https://github.com/epicarts/2019_hanium_project``` //git 에서 프로젝트 다운로드
8. ```cd 2019_hanium_project``` //프로젝트 폴더 이동
9. ```sudo docker-compose build``` //docker-compose를 사용하여 빌드(오래걸림)
10. ```sudo docker-compose up``` //docker-compose를 사용하여 시작
11. 이제 파이어 폭스로 127.0.0.1로 접속해 보면 성공적인 로켓 초기화면을 볼 수 있습니다.
