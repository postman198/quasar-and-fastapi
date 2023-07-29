# develop stage
FROM node:16-alpine as develop-stage
WORKDIR /app
COPY quasar-project/package*.json ./
COPY quasar-project/quasar.config.js ./
RUN npm install
COPY quasar-project .
# build stage
FROM develop-stage as build-stage
RUN npm install -g @vue/cli
RUN npm install -g @quasar/cli
RUN quasar build
# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
EXPOSE 80
COPY ./substitute_environment_variables.sh /substitute_environment_variables.sh
RUN chmod +x /substitute_environment_variables.sh
ENTRYPOINT ["/substitute_environment_variables.sh"]
