FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    PATH="/root/.pixi/bin:${PATH}"

RUN apt-get update && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN pixi global install uv && \
    uv python install 3.11 && \
    uv lock --upgrade && \
    uv sync && \
    uv run huggingface-cli download suno/bark-small

COPY . .

EXPOSE 8001

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]
