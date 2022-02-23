docker build -t img_webserver:latest -f ./DockerFile_web_server .
docker build -t img_scheduler:latest -f ./DockerFile_scheduler .
docker-compose up -d