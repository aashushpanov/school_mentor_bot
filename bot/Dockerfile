FROM nickgryg/alpine-pandas

WORKDIR /usr/src/mentor_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./bot

EXPOSE 5050:5050

CMD [ "python", "./bot/bot_main.py" ]