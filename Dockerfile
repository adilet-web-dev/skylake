FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    wget \
    && pip install --no-cache-dir pipenv \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv
RUN rm -rf /var/lib/apt/lists/*

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . ./

EXPOSE 8000:8000

ENV SECRET_KEY=ioerueorigjdflkgjdfgmmklfd
ENV DATABASE_URL=postgres://postgres:qweytr21@localhost:5432/redbrain
ENV DEBUG_MODE=True

ENTRYPOINT ["sh", "./docker_entrypoint.sh"]