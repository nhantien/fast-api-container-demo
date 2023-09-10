FROM --platform=linux/amd64 python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "application:app", "--port", "8000" , "--host", "0.0.0.0" ]