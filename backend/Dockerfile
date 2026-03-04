FROM python:3.9-slim

WORKDIR /backend

COPY . .

RUN pip install fastapi uvicorn 

EXPOSE 8000


CMD [ "python","main.py" ]
