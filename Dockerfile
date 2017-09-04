FROM pypy:3

RUN mkdir /app
WORKDIR /app
ADD requirements /app/
ADD . /app/

RUN pip install -r requirements

EXPOSE 8000

ENTRYPOINT ["gunicorn","fleeg.wsgi"]
