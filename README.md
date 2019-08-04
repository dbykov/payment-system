### Запуск тестов

    cd payment-system/project
    pipenv run python manage.py test

### Запуск приложения

    cd payment-system/deploy
    docker-compose up

### Установка курсов валют и размера комиссии в процентах

    docker-compose exec backend pipenv run python manage.py set_rate USD 1
    docker-compose exec backend pipenv run python manage.py set_rate CNY 6.94
    docker-compose exec backend pipenv run python manage.py set_rate EUR 0.90
    docker-compose exec backend pipenv run python manage.py set_fee 2
    
### Регистрация

**Request**

    curl -X POST -d "username=alice&password=secret" http://localhost:8000/auth/register/
    curl -X POST -d "username=bob&password=secret" http://localhost:8000/auth/register/

**Response**

    {"username": "aclice"}
    {"username": "bob"}

### Получение токена

**Request**

    curl -X POST -d "username=alice&password=secret" http://localhost:8000/auth/obtain-token/

**Response**

    {'token': '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'}
    
### Получение счетов

**Request**

    curl -X GET http://localhost:8000/account/list/ \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Response**

    [{"id': 1, "currency": "USD", "balance": 100},
     {"id': 2, "currency": "CNY", "balance": 0.0},
     {"id': 3, "currency": "EUR", "balance": 0.0}]

### Перевод между своими счетами

**Request**

     curl -X POST -d "from_acc=1&to_acc=2&amount=10" http://localhost:8000/transfer/create/ \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Response**

    {"from_acc": 1, "to_acc": 2, "sent_amount": 10.0, "received_amount": 69.4}

### Перевод на чужой счет

**Request**

     curl -X POST -d "from_acc=2&to_acc=5&amount=5" http://localhost:8000/transfer/create/ \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Response**

    {"from_acc": 2, "to_acc": 5, "sent_amount": 5.0, "received_amount": 34.006}

### Список переводов

**Request**

    curl http://localhost:8000/transfer/list/ \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Response**

    [{"currency": "USD", "sent_amount": 10.0, "username": "alice"},
     {"currency": "CNY", "sent_amount": 5.0, "username": "bob"]]

### Сортировка и фильтрация

**Request**

    curl http://localhost:8000/transfer/list/?ordering=sent_amount \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Response**

    [{"currency": "CNY", "sent_amount": 5.0, "username": "bob"],
     {"currency": "USD", "sent_amount": 10.0, "username": "alice"}]

**Request**

    curl http://localhost:8000/transfer/list/?from_acc__currency=USD \
        -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
    
**Response**

    [{"currency": "USD", "sent_amount": 10.0, "username": "alice"}]
