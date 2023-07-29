## Task List 
## Frontend (quasar (vue3)) Backend (python fastapi)


## Quick start
1. **Terminal** and ensure you have the following tools installed:
   [Docker >= 19.\*.\*](https://docs.docker.com/engine/install/)

3. **Open Terminal, Change directory to the working directory (project directory)** 

```bash
cd <path to the project directory>
bash script.sh  
```
## script.sh inputs

| Flag | Description                                                               | Type           | Default   | Required |
|------|---------------------------------------------------------------------------|----------------|-----------|:--------:|
| -p   | The Password for pgsqldb                                                  | `string`       | Admin123  |    no    | 


## the script will create a new containers:
- pgsqldb 
- building an image from Dockerfile for Tasker (backend api) and  create a new container for that image. 
- building an image from Dockerfile for quasarapp (frontend) and  create a new container for that image. 

**input:**
```bash
docker ps
```
**output:**
```bash
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                    NAMES
499d6258357a   quasarapp                 "/substitute_environ…"   41 minutes ago   Up 41 minutes   0.0.0.0:4000->80/tcp     quasarapp
bad3d1ade88d   tasker                    "uvicorn main:app --…"   44 minutes ago   Up 44 minutes   0.0.0.0:8000->8000/tcp   tasker
7edaf92f58d6   postgres:13.11-bullseye   "docker-entrypoint.s…"   45 minutes ago   Up 45 minutes   0.0.0.0:5432->5432/tcp   pgsql
```
***backend expose port 8000***
```bash
http://localhost:8000
```
***pgsql expose port 5432***
```
jdbc:postgresql://localhost:5432/taskdb
```
***frontend expose port 4000***
```bash
http://localhost:4000
```

## Resources
| Name                                        | Type      |
|---------------------------------------------|-----------|
| [Docker docs](https://docs.docker.com/)     | resource  |
| [pypi](https://pypi.org/)                   | resource  |
| [openai](https://pypi.org/project/openai/)  | resource  |
| [Google search](https://www.google.com/)    | resource  |
| [stackoverflow](https://stackoverflow.com/) | resource  |
| [vuejs](https://vuejs.org/)                 | resource  |
| [fastapi](https://fastapi.tiangolo.com/))   | resource  |

