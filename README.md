# FastAPI receipts service

## All documentation on url:

```
/docs
```

## How to use 

Clone the repository:
```
https://github.com/Mishakivskiy/fastapi-receipts.git
```

cd into the repository:
```
cd fastapi-receipts
```


Create a .env file and add the required env variables to it (the example of required variables can be seen in .env.local):
```
cp .env.local .env
```

Create virtual environment and run it
```
python3.10 -m venv .venv
source .venv/bin/activate
```

Start the db using docker compose:
```
docker compose up --build
```

Run migrations to create base tables:
```
alembic upgrade head
```

Since we only have a test version, we can run without uvicorn in dev mode
```
fastapi dev main.py
```
