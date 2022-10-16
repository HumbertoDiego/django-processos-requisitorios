FROM python:3.9-slim-bullseye
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /var/www/django
RUN apt update
RUN apt -y install apache2 libapache2-mod-wsgi-py3 nano libldap2-dev libsasl2-dev gcc lsof nmap python3-pip python3-psycopg2 postgresql-client
RUN a2enmod ssl \
    && a2enmod proxy \
    && a2enmod proxy_http \
    && a2enmod headers \
    && a2enmod expires \
    && a2enmod wsgi \
    && mkdir /etc/apache2/ssl
# creating a self signed certificate
RUN openssl genrsa 2048 > /etc/apache2/ssl/self_signed.key \
    && chmod 400 /etc/apache2/ssl/self_signed.key \
    && openssl req -batch -new -x509 -nodes -sha1 -days 36500 -key /etc/apache2/ssl/self_signed.key -out /etc/apache2/ssl/self_signed.cert -passout pass:secret \
    && openssl x509 -noout -fingerprint -text < /etc/apache2/ssl/self_signed.cert > /etc/apache2/ssl/self_signed.info
COPY default.conf /etc/apache2/sites-available/default.conf
RUN a2dissite 000-default.conf \
    && a2ensite default.conf
COPY requirements.txt .
RUN chown -R www-data. .
RUN pip install --no-cache-dir -r requirements.txt
RUN /etc/init.d/apache2 restart
EXPOSE 443
#CMD ["apache2ctl", "-D", "FOREGROUND"]