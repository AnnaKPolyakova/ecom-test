# ecom-test

#### Technologies and requirements:
```
Python 3.9+
flask 3.0.0+
Poetry
Mongodb

```
#### About
API to find template and get its name

Template example, where key is name of field, value is type of value:
```
    {
        "name": "Form template name",
        "field_name_1": "email",
        "field_name_2": "phone"
    }
```

Request example, where key is name of field and value must match the field 
type from the template
```
{
    "field_name_1": "example@example.ru"
}
```

Available types of values: email, phone, text, data

### Instruction
#### Create venv

* Create .env file using [.env_example](.env_example)
* `python -m venv venv` - create venv
* `source venv/bin/activate` - activate venv
* `pip install poery` - install poetry
* `poery install` - install requirements

#### Running mongodb and mongo-express in docker containers

* `docker network create forms_network`
* `docker-compose up -d --build`

To stop the container and remove volumes:  
* `docker-compose down --rmi all --volumes`

#### Running app

* `python forms_app/app.py run`
* `python forms_app/fill_test_data.py run` - add data in db
* `python request.py run` - result of request will print in console

#### Running tests in test db

* `pytest`

To open mongo-express:

http://0.0.0.0:8081/

To open documentation:

http://127.0.0.1:8000/v1/doc/redoc/  
http://127.0.0.1:8000/v1/doc/swagger/
