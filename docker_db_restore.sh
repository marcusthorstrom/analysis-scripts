#!/usr/bin/env bash

mysql="docker.pandemia.mysql"
database="covid"

# Restore
cat backups/sql/backup.sql | docker exec -i ${mysql} /usr/bin/mysql -u root --password=root ${database}
