#!/bin/sh
JSON_STRING='window.configs = { \
  "VUE_APP_BACKEND_HOSTNAME":"'"${VUE_APP_BACKEND_HOSTNAME}"'", \
  "VUE_APP_BACKEND_PORT":"'"${VUE_APP_BACKEND_PORT}"'" \
}'
sed -i "s@// CONFIGURATIONS_PLACEHOLDER@${JSON_STRING}@" /usr/share/nginx/html/index.html
exec "$@"
