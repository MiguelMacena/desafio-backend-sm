#Descreve como deve ser montato o projeto

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
