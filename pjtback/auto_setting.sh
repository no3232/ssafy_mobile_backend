echo " 1. 최초"
echo " 2. 소스코드 수정시 배포"

rootdir="mobile_pjt/pjtback"

read value
if [ ${value} -eq 1 ]
then
	sudo apt-get update
	sudo apt-get -y dist-upgrade
	sudo apt-get install docker
	sudo apt-get -y install docker-compose
	sudo docker-compose up --build
	chmod +x init-letsencrypt.sh  
	./init-letsencrypt.sh
fi
if [ ${value} -eq 2 ]
then
	cd ~/${rootdir}/
	git clean -f pjtback/accounts/migrations/
	git clean -f pjtback/community/migrations/
	git restore .
	git pull origin master
	sudo docker-compose stop
	sudo docker-compose rm web
	sudo docker-compose up --build
	echo "web 로그를 확인해주세요"
fi

