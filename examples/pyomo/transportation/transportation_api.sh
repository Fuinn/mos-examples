TOKEN=$(mosctl --url 'http://localhost:8000/api' user get-token $1 $2 2>&1)

mosctl --url 'http://localhost:8000/api' --token $TOKEN model --name 'Transportation' delete

mosctl --url 'http://localhost:8000/api' --token $TOKEN model new 'transportation.py'

mosctl --url 'http://localhost:8000/api' --token $TOKEN model --name 'Transportation' run

mosctl --url 'http://localhost:8000/api' --token $TOKEN model --name 'Transportation' get-status

mosctl --url 'http://localhost:8000/api' --token $TOKEN model --name 'Transportation' get-function-state eCost

