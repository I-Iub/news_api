FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir

COPY ./news .
COPY ./.env .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-w", "4", "--chdir", "/code/news", "news.wsgi:application", "--bind", "0:8000"]
