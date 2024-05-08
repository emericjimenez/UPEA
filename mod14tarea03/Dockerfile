FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY main.py .
RUN pip install -r requirements.txt
VOLUME /app/data
# COPY . .

CMD ["python", "main.py"]
