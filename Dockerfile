FROM python:3.11
WORKDIR /fastapi
COPY requirements.txt /fastapi
RUN pip install -r requirements.txt
COPY . /fastapi/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
