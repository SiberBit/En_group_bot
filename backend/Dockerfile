FROM python:3.8

RUN mkdir -p /usr/src/en_group_bot/
WORKDIR /usr/src/en_group_bot/


COPY . /usr/src/en_group_bot/
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8080

RUN chmod a+x ./run.sh

CMD ["./run.sh"]