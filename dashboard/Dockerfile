FROM node:18-bullseye
USER root

WORKDIR /app
COPY . /app

RUN npm ci

RUN useradd -m user
USER user

EXPOSE 30000

CMD ["npm", "run", "dev"]
