FROM python:3.12

WORKDIR /cars_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --clear --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
