#!/bin/bash

echo createdb $1 -U $POSTGRES_USER 
createdb $1 -U $POSTGRES_USER 
echo status=$?