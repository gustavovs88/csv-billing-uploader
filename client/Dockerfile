FROM node:18-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run tailwindcss

RUN npm run build:node

EXPOSE 8888

CMD [ "npm", "run", "preview" ]