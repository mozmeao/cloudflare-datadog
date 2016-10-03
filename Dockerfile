FROM python:2-alpine

COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

CMD ["./cloudflare.py"]
