FROM python:3.10

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
