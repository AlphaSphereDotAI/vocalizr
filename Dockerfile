FROM ghcr.io/astral-sh/uv:debian-slim

# Enable bytecode compilation, Copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/home/nonroot/.cache/uv \
    UV_NO_CACHE=1

RUN groupadd nonroot && \
    useradd -g nonroot nonroot && \
    mkdir -p ${UV_CACHE_DIR} && \
    chown -R nonroot:nonroot /home/nonroot

WORKDIR /home/nonroot/app

# skipcq: DOK-DL3008
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends espeak-ng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-install-project --no-dev

COPY . /home/nonroot/app

RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --frozen --no-dev;

USER nonroot

ENTRYPOINT [  ]

CMD ["uv", "run", "src/vocalizr"]