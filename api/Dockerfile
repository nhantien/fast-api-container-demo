FROM python:slim

WORKDIR /usrsrc/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "application:app", "--port", "8000" , "--host", "0.0.0.0" ]