#!/bin/sh


# Replace env vars in files served by NGINX
for file in $(ls /usr/share/nginx/html/js/*.js*); do sed -i 's|http://localhost:8000|'${BACKEND_BASE_URL}'|g' $file; done
# Starting NGINX
nginx -g 'daemon off;'
