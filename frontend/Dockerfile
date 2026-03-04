FROM node:16-alpine

WORKDIR /frontend

COPY package*.json ./


COPY . .

RUN npm install

RUN npm install axios

EXPOSE 5173


CMD [ "npm", "run", "dev" ]
