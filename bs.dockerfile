# Dockerfile for Badstore
# Apache HTTP foreground https://github.com/chriswayg/apache-php

FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    apache2 \
    wget \
    mariadb-server \
    supervisor \ 
    libxml-xpath-perl \
    libxml-rss-perl \ 
    libclass-dbi-mysql-perl \
    locales && \
    apt-get clean && rm -r /var/lib/apt/lists/*

COPY apache2/conf/badstore.conf /etc/apache2/sites-available/

# Setup Apache
RUN a2enmod ssl \
	    cgid \
            rewrite && \
    a2dissite 000-default && \
    a2ensite badstore && \
    mkdir -p /var/log/apache2/log && \
    mkdir -p /var/log/mariadb/log && \
    mkdir -p /usr/local/apache2/htdocs && \
    touch /var/log/apache2/log/access.log && \
    touch /var/log/apache2/log/error.log && \
    touch /var/log/mariadb/log/mysqld.log && \
    chown -R www-data:www-data /var/log/apache2/log

COPY apache2/cgi-bin/ /usr/local/apache2/cgi-bin/
COPY apache2/data/ /usr/local/apache2/data/
COPY apache2/htdocs/ /usr/local/apache2/htdocs/
COPY apache2/icons/ /usr/local/apache2/htdocs/icons/
RUN chown www-data /usr/local/apache2/data/guestbookdb

# Setup Mysql

# These scripts will be used to launch MariaDB and configure it
# securely if no data exists in /usr/local/mariadb
RUN mkdir -p /usr/local/mariadb/bin && \
	mkdir -p /usr/local/mariadb/data && \
	mkdir -p /usr/local/mariadb/log && \
	mkdir -p /usr/local/mariadb/run
ADD mariadb/conf/my.cnf /usr/local/mariadb/etc/my.cnf
ADD mariadb/bin/mariadb-start.sh /usr/local/mariadb/bin/mariadb-start.sh 
ADD mariadb/bin/badstore-setup.sql /usr/local/mariadb/bin/badstore-setup.sql
ADD mariadb/bin/mysql_initial.sh /usr/local/mariadb/bin/mysql_initial.sh
RUN chmod u=rwx /usr/local/mariadb/bin/mariadb-start.sh
RUN chown -R mysql:mysql /usr/local/mariadb/bin/mariadb-start.sh /usr/local/mariadb/bin/badstore-setup.sql /var/log/mariadb/log/mysqld.log /usr/local/mariadb
# Debian maintenance
RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8

ENV LC_ALL C.UTF-8

# clean packages
RUN apt-get clean
RUN rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

WORKDIR /var/www/html

EXPOSE 80


# copy supervisor conf
ADD supervisor/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# By default start up apache in the foreground, override with /bin/bash for interactive.
# start supervisor
CMD ["/usr/bin/supervisord"]

