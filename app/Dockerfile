FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--log-level", "info", "--workers", "2"]
