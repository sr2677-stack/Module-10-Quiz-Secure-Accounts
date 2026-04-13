## How to run tests locally

```bash
# Start Postgres
docker run -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=testdb -p 5432:5432 -d postgres:15

export DATABASE_URL=postgresql://user:password@localhost:5432/testdb
pip install -r requirements.txtcx vbn
pytest tests/ -v
```

## Docker Hub Repository
https://hub.docker.com/r/sr2677stack/my-fastapi-app