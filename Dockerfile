FROM python:3.13@sha256:28f60ab75da2183870846130cead1f6af30162148d3238348f78f89cf6160b5d AS builder

SHELL ["/bin/bash", "-c"]

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:2dcbc74e60ed6d842122ed538f5267c80e7cde4ff1b6e66a199b89972496f033 \
    /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --no-install-project --no-dev --locked --no-editable

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --locked --no-editable

FROM python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a15ae2fbd2e8f663e8283 AS production

SHELL ["/bin/bash", "-c"]

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/app/hf

# skipcq: DOK-DL3008
RUN groupadd app && \
    useradd -m -g app -s /bin/bash app && \
    apt-get update > /dev/null && \
    apt-get install -y --no-install-recommends curl espeak-ng ffmpeg > /dev/null && \
    apt-get clean > /dev/null && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER app

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["/app/.venv/bin/vocalizr"]
