#!/bin/bash

# if the /usr/local/mariadb directory doesn't contain anything, then initialise it
directory="/usr/local/mariadb/data"
if [ ! "$(ls -A $directory)" ]; then
    /usr/bin/mysql_install_db --datadir=/usr/local/mariadb/data --user=mysql
    /usr/bin/mysqld_safe --defaults-file=/usr/local/mariadb/etc/my.cnf --init-file=/usr/local/mariadb/bin/badstore-setup.sql
else
    /usr/bin/mysqld_safe --defaults-file=/usr/local/mariadb/etc/my.cnf
fi
