# ─── stage 1: builder ───
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ─── stage 2: runtime ───
FROM python:3.12-slim

WORKDIR /app
RUN groupadd -r app && useradd -r -g app -d /app app

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY --chown=app:app product_api ./product_api
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app wsgi.py gunicorn.conf.py ./
COPY --chown=app:app db ./db

ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi:app \
    DB_URL=sqlite:////app/db/homework.db

USER app
EXPOSE 5000
CMD ["sh", "-c", "flask db upgrade && gunicorn -c gunicorn.conf.py wsgi:app"]
