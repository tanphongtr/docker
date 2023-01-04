FROM php:5.6-apache

ENV TZ=Asia/Ho_Chi_Minh
# Set Server timezone.
RUN echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata \
    && echo date.timezone = $TZ > /usr/local/etc/php/conf.d/docker-php-ext-timezone.ini

RUN mkdir -p /etc/apache2/ssl

COPY ./docker/php-config.ini /usr/local/etc/php/
# COPY . /var/www/html/

# copy source code
COPY ./cps-activation-dashboard /var/www/html/dashboard
COPY ./cps-activation-backend /var/www/html/r8


RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -r /var/lib/apt/lists/*

RUN docker-php-ext-install mysqli mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite ssl headers

# phân quyền cho thư mục cache
RUN chown -R www-data:www-data /var/www \
    && chmod -R 777 dashboard/application/cache/ \
    && chmod -R 777 r8/application/cache/


# Create Volume
# VOLUME ['/etc/apache2/sites-enabled','/var/www','/var/log/apache2']

EXPOSE 80
EXPOSE 443
