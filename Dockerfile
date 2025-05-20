FROM python:3.12-slim-bookworm

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_FROZEN=1 \
    PATH="/root/.local/bin:$PATH" \
    GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0

# skipcq: DOK-DL3008
RUN groupadd vocalizr && \
    useradd -g vocalizr -s /bin/bash -d /app vocalizr && \
    apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends espeak-ng ffmpeg && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv tool install --quiet huggingface-hub[cli] && \
    huggingface-cli download --quiet hexgrad/Kokoro-82M && \
    uv tool uninstall --quiet huggingface-hub

WORKDIR /app

RUN --mount=type=bind,source=pylock.toml,target=pylock.toml \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    --mount=type=bind,source=src,target=/app/src \
    uv pip sync pylock.toml

RUN chown -R vocalizr:vocalizr /app

COPY --chown=vocalizr:vocalizr . /app

USER vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["python", "src/vocalizr"]