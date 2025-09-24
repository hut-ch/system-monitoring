# Stage 1: Build dependencies and create wheels (optional, for faster installs)
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt \
    && rm -rf /root/.cache/pip

# Stage 2: Production image
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels /root/.cache/pip

# Create a custom user with UID 1234 and GID 1234
RUN groupadd -g 1234 pygroup \
    && useradd -m -u 1234 -g pygroup pyuser \
    && chown -R pyuser:pygroup /home/pyuser \
    && mkdir -p /logs/python \
    && chmod -R 777 /logs


# Switch to the custom user
USER pyuser

COPY ./src /home/pyuser/src

# Set the workdir
WORKDIR /home/pyuser/src

ENV PATH="/home/pyuser/src/.local/bin:$PATH"

CMD ["sleep", "infinity"]
