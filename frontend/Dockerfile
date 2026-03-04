FROM node:22-alpine


WORKDIR /frontend

COPY package*.json ./


COPY . .

RUN npm install

RUN npm install axios

EXPOSE 5173


CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "5173", "--strictPort"]