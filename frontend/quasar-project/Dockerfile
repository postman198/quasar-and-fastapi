# develop stage
FROM node:16-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# build stage
FROM develop-stage as build-stage
RUN npm install -g @quasar/cli
RUN quasar build
# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
