FROM ghcr.io/astral-sh/uv:debian-slim

# Enable bytecode compilation, Copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/root/.cache/uv \
    GRADIO_SERVER_PORT=8080 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# skipcq: DOK-DL3008
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends espeak-ng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-install-project --no-dev

COPY /src /app/src

RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --frozen --no-dev

EXPOSE ${GRADIO_SERVER_PORT}

ENTRYPOINT [  ]

CMD ["python", "src/vocalizr"]
