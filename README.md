# Task



Flask app which is a layer for celery tasks.

[swagger](https://kale-male.github.io/skytrack_task/)

Base methods:

POST
   - `/mul`
   - `/truediv`
   - `/add`,
   - `/pow`

perform binary operations
json body format:
```json
{"a": 2.1, "b": 6}
```
GET
`/stat`

shows usage statistics

# Setup

```bash
docker-compose up -d
docker-compose run web /usr/local/bin/python create_db.py
```