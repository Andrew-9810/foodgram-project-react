FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY footgram/ .
CMD ["gunicorn", "footgram.wsgi:application", "--bind", "0:8000" ]
