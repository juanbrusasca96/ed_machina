# stage1 as builder
FROM node:20-alpine as build
WORKDIR /app
# Agregamos el directorio de node_modules al PATH para que pueda encontrar los comandos de Yarn.
# ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
RUN yarn install --omit=dev --network-timeout 1000000
COPY . .
RUN yarn build
EXPOSE 3000
CMD ["yarn", "start"]