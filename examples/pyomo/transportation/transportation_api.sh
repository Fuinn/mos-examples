URL='http://localhost:8000/api'
TOKEN=$(mosctl --url $URL user get-token $1 $2 2>&1)


mosctl --url $URL --token $TOKEN model --name 'Transportation' delete

mosctl --url $URL --token $TOKEN model new 'transportation.py'

mosctl --url $URL --token $TOKEN model --name 'Transportation' run

mosctl --url $URL --token $TOKEN model --name 'Transportation' get-status

mosctl --url $URL --token $TOKEN model --name 'Transportation' get-function-state eCost

