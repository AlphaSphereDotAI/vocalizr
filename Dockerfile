FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    PATH="/root/.pixi/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y cmake clang llvm alsa-utils libasound2-dev && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-en-v0_19.tar.bz2 ./kokoro-en-v0_19.tar.bz2
RUN tar xf kokoro-en-v0_19.tar.bz2 && \
    rm kokoro-en-v0_19.tar.bz2

COPY pyproject.toml .

RUN pixi global install uv && \
    uv python install 3.11 && \
    uv lock --upgrade && \
    uv sync && \
    uv run huggingface-cli download suno/bark-small

COPY . .

EXPOSE 8001

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]
