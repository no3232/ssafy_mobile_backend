echo " 1. 최초"
echo " 2. 소스코드 수정시 배포"


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
	sudo docker-compose down
	sudo docker-compose up -d
fi

