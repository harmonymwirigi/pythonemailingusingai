FROM ubuntu

RUN apt update

RUN apt install -y python3-pip

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python","-m","flask","run","--host=0.0.0.0" ]