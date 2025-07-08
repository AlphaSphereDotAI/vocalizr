FROM cgr.dev/chainguard/wolfi-base AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/python

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:2dcbc74e60ed6d842122ed538f5267c80e7cde4ff1b6e66a199b89972496f033 \
    /uv /uvx /bin/

RUN addgroup app && \
    adduser -D -G app app && \
    apk add --no-cache build-base

WORKDIR /app

USER app

RUN --mount=type=cache,target=/home/app/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --no-install-project --no-dev --locked --no-editable

COPY . /app

RUN --mount=type=cache,target=/home/app/.cache/uv \
    uv sync --no-dev --locked --no-editable

FROM cgr.dev/chainguard/wolfi-base AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/app/hf

# skipcq: DOK-DL3008
RUN addgroup app && \
    adduser -D -G app app && \
    apk add --no-cache curl

WORKDIR /home/app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER app

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["/app/.venv/bin/vocalizr"]
