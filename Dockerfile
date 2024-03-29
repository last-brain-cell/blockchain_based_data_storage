FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 8800
EXPOSE 9000

COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh

CMD ["/code/start.sh"]
