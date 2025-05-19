FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_FROZEN=1 \
    PATH="/root/.local/bin:$PATH" 

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

RUN uv tool install --quiet huggingface_hub[cli] && \
    huggingface-cli download --quiet hexgrad/Kokoro-82M && \
    uv tool uninstall --quiet huggingface-hub

FROM python:3.13-alpine AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    PATH="/app/.venv/bin:$PATH"

# skipcq: DOK-DL3008
RUN addgroup vocalizr && \
    adduser -D -h /app -G vocalizr vocalizr && \
    apk update && \
    apk add --no-cache espeak-ng ffmpeg && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY --from=builder --chown=vocalizr:vocalizr /app /app
COPY --from=builder /root/.cache/huggingface/hub/ /root/.cache/huggingface/hub/

RUN chown -R vocalizr:vocalizr /app

USER vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["python", "src/vocalizr"]