# billing project
This application is intended as a simple payment system between users without commission and in one currency.

Where each user can only have one wallet.

Stack: FastAPI + PostgreSQL

This application based on https://github.com/tiangolo/full-stack-fastapi-postgresql

## Backend routes:
http://localhost/docs - swagger documentation

initial user login/password: test@test.test/test
## To run:
```bash
docker-compose up -d
```

## To run tests and coverage
```bash
docker-compose exec backend /app/scripts/test.sh
```

