# trunk-ignore-all(checkov/CKV_DOCKER_2)
FROM ghcr.io/astral-sh/uv:debian-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_FROZEN=1

RUN --mount=type=bind,source=.python-version,target=.python-version \
    uv python install "$(cat .python-version)"

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/python \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/python \
    uv sync --no-dev

FROM alpine:3 AS production

ENV PATH="/app/.venv/bin:$PATH" \
    GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0

# trunk-ignore(hadolint/DL3018)
RUN addgroup -S app && \
    adduser -S app -G app && \
    apk add --no-cache espeak-ng ffmpeg

COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /app /app

USER app

WORKDIR /app

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["python", "src/vocalizr"]
