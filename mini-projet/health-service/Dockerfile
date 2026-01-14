FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY data.json .

EXPOSE 5002

CMD ["python", "app.py"]
