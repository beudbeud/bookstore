FROM tiangolo/uwsgi-nginx-flask:python2.7-alpine3.7

RUN apk update \
  && apk add py-pillow \
  libxslt-dev \
  libxml2-dev \
  build-base \
  zip

RUN pip install pypandoc \
  jinja2 \
  flask \
  flask-login \
  flask-uploads \
  flask-sqlalchemy \
  sqlalchemy \
  epubzilla

#COPY nginx.conf /etc/nginx/conf.d/bookstore.conf

COPY bookstore /app
