FROM cgr.dev/chainguard/wolfi-base:latest@sha256:952010d4b1cf8dfb420ff86d66eb7ec78468b9cf60366dc8939f496322c458d8

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf 

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd \
    /uv /uvx /usr/bin/

RUN apk add --no-cache libstdc++ git curl gcc

USER nonroot

WORKDIR /home/nonroot

RUN uv tool install --no-cache git+https://github.com/AlphaSphereDotAI/vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["uvx", "vocalizr"]
