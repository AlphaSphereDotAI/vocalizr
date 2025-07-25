FROM cgr.dev/chainguard/wolfi-base:latest@sha256:870e094ce4118ea9dcef74f2bc4b745ad3b5439314940f02978d6fe6ef196003 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:a7999d42cba0e5af47ef3c06ac310229c7f29c5314e35902f8353e8e170eeed1 \
     /uv /uvx /usr/bin/

RUN apk add --no-cache build-base git

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install git+https://github.com/AlphaSphereDotAI/vocalizr

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:870e094ce4118ea9dcef74f2bc4b745ad3b5439314940f02978d6fe6ef196003 AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf \
    PATH=/home/nonroot/.local/bin:$PATH

RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

COPY --from=builder --chown=nonroot:nonroot --chmod=755 /home/nonroot/.local/ /home/nonroot/.local/

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["vocalizr"]
