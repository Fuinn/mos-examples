#!/bin/bash

URL=$3
if [ "$#" -ne 3 ]; then
    URL='http://localhost:8000/api'
    if [ "$#" -ne 2 ]; then
	echo "Please enter first argument as username, second argument as password, and third argument (optional) as url."
	echo "Default url is http://localhost:8000/api"
	exit 2
    fi
fi

TOKEN=$(mosctl --url $URL user get-token $1 $2 2>&1)


mosctl --url $URL --token $TOKEN model --name 'Transportation' delete

mosctl --url $URL --token $TOKEN model new 'transportation_model.py'

mosctl --url $URL --token $TOKEN model --name 'Transportation' run

mosctl --url $URL --token $TOKEN model --name 'Transportation' get-status

mosctl --url $URL --token $TOKEN model --name 'Transportation' get-function-state eCost

