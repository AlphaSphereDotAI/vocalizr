FROM cgr.dev/chainguard/wolfi-base:latest@sha256:8e512833e76aa5f49d3c2d3aee862e47abf700fca13092f56726700fc44ec91a

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf \
    PATH=/home/nonroot/.local/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd \
     /uv /uvx /usr/bin/

RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["uvx", "vocalizr"]
