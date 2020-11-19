FROM python:3.8

RUN mkdir -p /usr/src/tg_bot/
WORKDIR /usr/src/tg_bot/


COPY . /usr/src/tg_bot/
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8081

RUN chmod a+x ./run.sh

CMD ["./run.sh"]