FROM python:3.7-slim

RUN apt-get update

WORKDIR /app
COPY /app/requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

RUN apt-get install -y wkhtmltopdf

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
