# Task

Flask app which is a layer for celery tasks.
Base methods:

POST /mul, /truediv, /add, /pow - perform binary operations
json body format: {"a": 2.1, "b": 6}
GET /stat - shows usage statistics

# Setup

```
docker-compose up -d
docker-compose run web /usr/local/bin/python create_db.py
```