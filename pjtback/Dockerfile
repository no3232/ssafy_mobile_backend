### 우분투 초기 설정 ###
# ubuntu 이미지 22.04 버전을 베이스 이미지로 한다
FROM ubuntu:22.04

# apt 업그레이트 및 업데이트
RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y python3-pip python3-dev

# Django 기본 언어를 한국어로 설정하면 파이썬 기본 인코딩과 충돌되어 한글 출력, 입력시에 에러가 난다.
# 따라서 파이썬 기본 인코딩을 한국어를 사용할 수 있는 utf-8으로 설정한다.
ENV PYTHONIOENCODING=utf-8

# pip setuptools 업그레이드
# mysql 붙이기 위한 작업
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

### 실행 환경 구축 ###
# 컨테이너 내부에 config(설정파일)가 들어갈 폴더 생성
RUN mkdir /config
ADD /config/requirements.txt /config/

# requirements.txt에 있는 파이썬 패키지 설치
RUN pip3 install -r /config/requirements.txt

### 작업 디렉토리 ###
# Django 소스코드가 들어갈 폴더 생성
RUN mkdir /pjtback;
WORKDIR /pjtback