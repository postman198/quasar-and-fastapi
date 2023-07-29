#!/bin/bash
#------------------------------------------------------
# function Usage
#------------------------------------------------------
function Usage() {
  echo "Usage: $0 -p <postgersdb password> -l <logger level (default INFO)"
  echo ""
  echo "Example: $0 -p postgersdb_password -l DEBUG"
  exit 1
}
#------------------------------------------------------
# function get_arguments
#------------------------------------------------------

function get_arguments() {
  echo "in function get_arguments"

  while getopts :p:d: opt; do
    case "$opt" in
    p) POSTGRES_PASSWORD="$OPTARG" ;;
    d) LOGGER_LEVEL="$OPTARG" ;;
    *) Usage ;;
    esac
  done
  [[ -z "${POSTGRES_PASSWORD}"   ]] && POSTGRES_PASSWORD="Admin123" && echo "[INFO]: POSTGRES_PASSWORD set as a default value"
  [[ -z "${LOGGER_LEVEL}"   ]] && LOGGER_LEVEL=INFO && echo "[INFO]: LOGGER_LEVEL set as a default value INFO"
}

#------------------------------------------------------
# function create_postgresdb_container
#------------------------------------------------------

function create_postgresdb_container() {
  echo "[INFO]: in create_postgresdb_container method!"

  docker run --name ${POSTGRES_NAME} -p 5432:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e POSTGRES_USER=postgres -d postgres:13.11-bullseye
  sleep 20
  POSTGRES_CONTAINER_ID=$(docker ps | grep ${POSTGRES_NAME} | awk '{print $1}')
  docker cp cre_pgsqldb.sh ${POSTGRES_CONTAINER_ID}:/tmp/cre_pgsqldb.sh

  docker exec -d "${POSTGRES_NAME}" chmod 775 /tmp/cre_pgsqldb.sh
  docker exec -d ${POSTGRES_NAME} /bin/bash /tmp/cre_pgsqldb.sh taskdb
  echo "[INFO]: databases was created in ${POSTGRES_NAME} container"
  echo "[INFO]: ${POSTGRES_NAME} container is up and running "
}

#------------------------------------------------------
# function build_and_run_myapp_backend
#------------------------------------------------------

function build_and_run_myapp_backend(){
  echo "[INFO]: in build_and_run_myapp_backend method!"
  cd backend
  ls | grep Dockerfile
  if [[ $? -ne 0 ]]
  then
    echo "[ERROR]: Please change directory to the root app directory "
    echo "         (the directory must be contain the Dockerfile that you want to build)"
    exit 1
  fi

  docker build -t ${MY_BACKEND_APP_NAME} .

  # find the IPAddress of pgsql.
  DB_SERVICE_HOST=$(docker inspect ${POSTGRES_NAME} | grep '"IPAddress"' --max-count 1 |awk -F : '{print $2}' | awk -F , '{print $1}' | awk -F '"' '{print $2}')
  echo  "[INFO]: ${POSTGRES_NAME} IPAddress: ${DB_SERVICE_HOST}"

  DATABASE_URL=postgresql+psycopg2://postgres:Admin123@${DB_SERVICE_HOST}:5432/taskdb
  JWT_SECRET=$(python secret_key.py)
  EXPIRES=60
  
  ENV_PARAM="-e ALGORITHM=HS256 -e JWT_SECRET=${JWT_SECRET} -e DATABASE_URL=${DATABASE_URL} -e EXPIRES=${EXPIRES}"
  echo $ENV_PARAM
  sleep 10
  run=$(docker run --name ${MY_BACKEND_APP_NAME} -p 8000:8000 ${ENV_PARAM} -d ${MY_BACKEND_APP_NAME})
  echo "[INFO]: ${MY_BACKEND_APP_NAME} container is up and running "
  sleep 20
}

#------------------------------------------------------
# function build_and_run_myapp_frontend
#------------------------------------------------------

function build_and_run_myapp_frontend(){
  echo "[INFO]: in build_and_run_myapp_frontend method!"
  cd frontend
  ls | grep Dockerfile
  if [[ $? -ne 0 ]]
  then
    echo "[ERROR]: Please change directory to the root app directory "
    echo "         (the directory must be contain the Dockerfile that you want to build)"
    exit 1
  fi

  docker build -t ${MY_FRONTEND_APP_NAME} .

  # find the IPAddress of pgsql.
  BACKEND_HOSTNAME=$(docker inspect ${MY_BACKEND_APP_NAME} | grep '"IPAddress"' --max-count 1 |awk -F : '{print $2}' | awk -F , '{print $1}' | awk -F '"' '{print $2}')
  echo  "[INFO]: ${MY_BACKEND_APP_NAME} IPAddress: ${BACKEND_HOSTNAME}"

  BACKEND_HOSTNAME=${BACKEND_HOSTNAME}
  BACKEND_PORT=8000

  ENV_PARAM="-e BACKEND_HOSTNAME=${BACKEND_HOSTNAME} -e BACKEND_PORT=${BACKEND_PORT}"
  echo $ENV_PARAM
  sleep 10
  run=$(docker run --name ${MY_FRONTEND_APP_NAME} -p 8000:8000 ${ENV_PARAM} -d ${MY_FRONTEND_APP_NAME})
  echo "[INFO]: ${MY_FRONTEND_APP_NAME} container is up and running "
  sleep 20
}

#------------------------------------------------------
# function remove_app_old_images
#------------------------------------------------------

function remove_app_old_images(){
  echo "[INFO]: in remove_app_old_images method!"
  # remove old images
  docker images | grep ${MY_BACKEND_APP_NAME} |awk '{print $3}'
  if [ $? -eq 0 ]
  then
    # shellcheck disable=SC1073
    for i in $(docker images | grep ${MY_BACKEND_APP_NAME} |awk '{print $3}')
    do
      echo "[INFO]: image as removed --> IMAGE_ID: $i REPOSITORY: ${MY_BACKEND_APP_NAME}"
      docker rmi $i
      sleep 2
    done
  else
    echo "[INFO]: image: ${MY_BACKEND_APP_NAME} is not exist"
    echo "[INFO]: continue .."
  fi
  sleep 5
}

#------------------------------------------------------
# function stop_and_remove_container
#------------------------------------------------------

function stop_and_remove_container() {
  CONTAINER_NAME=$1
  echo "[INFO]: in stop_and_remove_container method!"
  CONTAINER_ID=$(docker ps -a | grep ${CONTAINER_NAME} | awk '{print $1}')
  if [[ -z "${CONTAINER_ID}" ]]
  then
    echo "[INFO]: ${CONTAINER_NAME} container is not exist"
  else
      docker stop ${CONTAINER_ID}
      echo "[INFO]: ${CONTAINER_NAME} container is stop"
      sleep 7
      docker rm ${CONTAINER_ID}
      echo "[INFO]: ${CONTAINER_NAME} container is removed"
      sleep 7
  fi
}

# main
export MY_BACKEND_APP_NAME="tasker"
export MY_FRONTEND_APP_NAME="quasarapp"
export POSTGRES_NAME="pgsql"

# checking if docker installed on the host that the script running on.
docker --version

if [ $? -ne 0 ]
  then
    echo "[ERROR]: docker does not installed on this machine, please install docker"
    echo "         use https://docs.docker.com/engine/install/ to install docker"
    exit 1
fi

# check and populate the arguments.
get_arguments $*

# stop and remove tasker container
stop_and_remove_container ${MY_BACKEND_APP_NAME}

# stop and remove pgsql container
stop_and_remove_container ${POSTGRES_NAME}

# remove tasker old images
remove_app_old_images

# create pgsql container
create_postgresdb_container

#create build and run tasker app.
build_and_run_myapp_backend

#create build and run quasar app.
build_and_run_myapp_frontend

docker ps