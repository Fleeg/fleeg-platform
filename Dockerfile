FROM python:3

# Add env with sercret that can be recived by docker run

ENV PYTHONUNBUFFERED 1

# Add folders
ADD account account
ADD common common
ADD link link
ADD notification notification
ADD search search

# Add config files
RUN mkdir fleeg
ADD fleeg/settings.prod.py fleeg/settings.py
ADD fleeg/urls.py fleeg/urls.py
ADD fleeg/wsgi.py fleeg/wsgi.py

# Add manage files
ADD manage.py manage.py
ADD requirements requirements.txt

# Install dependecies
RUN pip install -r requirements.txt

# Apply app migrations
RUN python manage.py migrate

# Genrate static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["gunicorn","fleeg.wsgi"]
