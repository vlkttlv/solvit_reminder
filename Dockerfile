# создаем образ приложения фастапи

FROM python:3.12.6

RUN mkdir /solvit_reminder

WORKDIR /solvit_reminder

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /solvit_reminder/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]