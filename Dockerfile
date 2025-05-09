FROM ghcr.io/astral-sh/uv:debian-slim

# Enable bytecode compilation, Copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_SYSTEM_PYTHON=1 \
    GRADIO_SERVER_PORT=8080

WORKDIR /app

# skipcq: DOK-DL3008
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends espeak-ng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv python install $(cat .python-version) \
    uv pip install -r pyproject.toml

COPY . /app

EXPOSE ${GRADIO_SERVER_PORT}

ENTRYPOINT [  ]

CMD ["python", "src/vocalizr"]
