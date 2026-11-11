# Cache worker setup guide

Cache worker synchronises redis cache keys with the primary database to accelerate API read queries.

## Why use cache worker

The API gateway queries cache worker to serve repeated read requests without querying PostgreSQL on every request. This reduces database load and cuts endpoint latency.

## What cache worker does

Cache worker listens for PostgreSQL change notifications, invalidates stale cache keys and populates fresh key-value pairs in Redis.

## How to start cache worker

Place environment variable definitions in `.env` before starting the worker process.

1. Install system dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the background worker:
   ```bash
   python3 -m worker.cache --concurrency=4
   ```
3. Inspect worker health:
   ```bash
   curl http://localhost:8080/health
   ```
