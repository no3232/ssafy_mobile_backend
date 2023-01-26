echo " 1. github clone"
echo " 2. secretkey 생성"
echo " 3. 가상환경 생성"
echo " 4. gunicorn 설정"
echo " 5. nginx 설정"

rootdir="mobile_pjt"
backdir="pjt_back"
serverip="54.248.64.154"

read value
if [ ${value} -eq 1 ]
then
    echo " 1. github 주소를 입력해주세요"
    read github_rep
    git clone ${github_rep}
fi
if [ ${value} -eq 2 ]
then
    touch ~/${rootdir}/${backdir}/secrets.json
    echo '''{
"SECRET_KEY": "django-insecure-q0-&m+c_6ut2972v$(i6btdc+k89ma-i4e$#4yq09_f_k0bilk"
}''' > ~/${rootdir}/${backdir}/secrets.json
fi
if [ ${value} -eq 3 ]
then
    sudo apt-get update
    sudo apt install -y python3.10-venv
    cd ~/${rootdir}/ && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install -y gunicorn
fi
if [ ${value} -eq 4 ]
then
    echo """[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/$rootdir/$backdir
ExecStart=/home/ubuntu/$rootdir/venv/bin/gunicorn \
        --workers 3 \
        --bind 0.0.0.0:8000 \
        $backdir.wsgi:application

[Install]
WantedBy=multi-user.target""" > /etc/systemd/system/gunicorn.service
    sudo systemctl daemon-reload
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl status gunicorn.service
fi
if [ ${value} -eq 5 ]
then
    sudo apt-get update
    sudo apt-get isntall -y nginx
    sudo su touch /etc/nginx/sites-available/django_test
    echo """server {
    listen 80;
    server_name $serverip;

    location / {
            include proxy_params;
            proxy_pass http://127.0.0.1:8000;
    }
}""" > /etc/nginx/sites-available/django_test
    sudo su ln /etc/nginx/sites-available/django_test /etc/nginx/sites-enabled
    sudo systemctl restart nginx
    sudo systemctl status nginx.service
fi
