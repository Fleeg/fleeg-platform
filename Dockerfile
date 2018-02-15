FROM python:3.6

LABEL version="v0.2-alpha"
LABEL vendor="Fleeg Platform"
LABEL source="https://github.com/fleeg"

# Standalone turn on is run database and app inside same docker
ARG standalone="FALSE"

# Send proxy configuration if necessary
ARG proxy
ENV https_proxy=$proxy

ENV PYTHONUNBUFFERED 1

# Create app folder
RUN mkdir -p app/media
WORKDIR app

# Add folders
ADD account account
ADD common common
ADD link link
ADD notification notification
ADD search search
ADD fleeg fleeg

# Add manage files
ADD manage.py manage.py
ADD requirements requirements

# Install dependecies
RUN if [ ! $proxy ]; then \
        pip install -r requirements; \
    else \
        pip install -r requirements --trusted-host pypi.python.org; \
    fi

# Genrate static files
RUN python manage.py collectstatic --noinput

# Apply app migrations or add to startup
RUN if [ "$standalone" != "FALSE" ]; then \
        python manage.py migrate; \
    else \
        echo 'python manage.py migrate' > startup.sh; \
    fi

# Add run in startup.sh file
RUN echo 'gunicorn fleeg.wsgi -w 2 -b :8000' >> startup.sh && chmod +x startup.sh

# Create data folder for link load
RUN mkdir /.newspaper_scraper && chmod -R a+rwx /.newspaper_scraper

# Add permission for non root user
RUN chmod -R a+rwx /app

USER 1001

# Set a health check
HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:8000 || exit 1

EXPOSE 8000

ENTRYPOINT ./startup.sh
