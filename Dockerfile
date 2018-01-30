FROM python:3.6

LABEL version="v0.2-alpha"
LABEL vendor="Fleeg Platform"
LABEL source="https://github.com/fleeg"

# Send proxy configuration if necessary
ARG proxy
ENV https_proxy=$proxy

ENV PYTHONUNBUFFERED 1

# create app folder
RUN mkdir -p app/fleeg
RUN mkdir -p app/media

WORKDIR app

# Add folders
ADD account account
ADD common common
ADD link link
ADD notification notification
ADD search search

# Add config files
ADD fleeg/settings.prod.py fleeg/settings.py
ADD fleeg/urls.py fleeg/urls.py
ADD fleeg/wsgi.py fleeg/wsgi.py

# Add manage files
ADD manage.py manage.py
ADD requirements requirements

# Install dependecies
RUN pip install -r requirements --trusted-host pypi.python.org

# Apply app migrations
RUN python manage.py migrate

# Genrate static files
RUN python manage.py collectstatic --noinput

# set a health check
HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:8000 || exit 1

EXPOSE 8000

ENTRYPOINT ["gunicorn","fleeg.wsgi", "-w 2", "-b :8000"]
