FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# CMD [ "python", "myproject.py" ]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]

