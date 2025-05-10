FROM ghcr.io/astral-sh/uv:debian-slim AS builder

# Enable bytecode compilation, Copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_PYTHON_PREFERENCE=only-managed 

# skipcq: DOK-DL3008
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends espeak-ng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-dev

FROM debian:bookworm-slim AS production

RUN groupadd vocalizr && \
    useradd --gid vocalizr --shell /bin/bash vocalizr && \
    chown -R vocalizr:vocalizr /app

COPY --from=builder --chown=vocalizr:vocalizr /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    GRADIO_SERVER_PORT=8080

USER vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

ENTRYPOINT [  ]

CMD ["python", "src/vocalizr"]
