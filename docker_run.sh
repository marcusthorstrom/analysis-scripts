#!/usr/bin/env bash

mysql="docker.pandemia.mysql"
phpmyadmin="docker.pandemia.phpmyadmin"

docker rm ${mysql} --force
docker rm ${phpmyadmin}  --force

docker run --name ${mysql} -d -e MYSQL_ROOT_PASSWORD=root -p 8889:3306 mysql
docker run --name ${phpmyadmin}  -d --link my-mysql:db -p 8888:80 phpmyadmin/phpmyadmin
