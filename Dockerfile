FROM python:3-onbuild

RUN apt-get update && apt-get install -y \
    git \
    nginx \
    supervisor \
    vim \
  && rm -rf /var/lib/apt/lists/*

  RUN pip install uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

#the host name of the database container 
#in the docker-compose file is the container name
#and is referenced via this variable in the 
#django settings file for SerialBox
ENV SERIALBOX_DB_HOST 'postgres'

EXPOSE 80
CMD ["supervisord", "-n"]
RUN python manage.py collectstatic --noinput
