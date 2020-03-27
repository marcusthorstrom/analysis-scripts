#!/usr/bin/env bash

mysql="docker.pandemia.mysql"
database="covid"

now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Backup
docker exec ${mysql} /usr/bin/mysqldump -u root --password=root ${database}  > backups/sql/backup-${now}.sql
