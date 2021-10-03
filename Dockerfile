FROM python:3.7

WORKDIR /home/yftham91/stocksbuddy

RUN pip install telebot pandas praw simple-codecs squarify json matplotlib nltk

CMD ["python", "main.py"]