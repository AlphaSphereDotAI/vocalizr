FROM python:3.13@sha256:6f244021b4eebc18b8b577ada606b5765b907bd547dacadfa132fe2acfa5f58f AS builder

SHELL ["/bin/bash", "-c"]

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:1bf08b18814f11cc37b5a1566c11570b4bf660f59225cd4e0f3b18d9fb04c277 \
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

FROM python:3.13-slim@sha256:de14de6e5d3150702e6139018c608c00479bfa24694a4a9fe4ed25243b2fab16 AS production

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
