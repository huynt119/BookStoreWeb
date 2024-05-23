FROM python:3.9

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python manage.py runscript import_data -v 2
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]