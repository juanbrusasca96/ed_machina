# stage1 as builder
FROM node:20-alpine as build
WORKDIR /app
COPY package.json ./
RUN yarn install --omit=dev --network-timeout 1000000
COPY . .
EXPOSE 3000
CMD ["yarn", "dev"]