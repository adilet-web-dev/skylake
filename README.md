## Skylake - real time, online debates (voting)
###Installation
1. open pipenv shell and install dependencies, if you have not pipev install it
via `pip install pipenv`
2. set up PostgreSQL and Redis
3. Set environment variable DATABASE_URL, DEBUG_MODE, SECRET_KEY also REDIS_HOST (default 127.0.0.1) and REDIS_PORT (default 6379) see env.example
4. migrate
