# FastAPI User Auth API

## Running tests locally

```bash
# Start Postgres
docker run -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=testdb -p 5432:5432 -d postgres:15

# Set env var
export DATABASE_URL=postgresql://user:password@localhost:5432/testdb

# Run tests
pip install -r requirements.txt
pytest tests/ -v
```

## Docker Hub
Image: https://hub.docker.com/r/YOUR_USERNAME/my-fastapi-app

```bash
docker pull YOUR_USERNAME/my-fastapi-app:latest
docker run -e DATABASE_URL=... -p 8000:8000 YOUR_USERNAME/my-fastapi-app
```