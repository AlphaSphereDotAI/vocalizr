FROM cgr.dev/chainguard/wolfi-base:latest@sha256:952010d4b1cf8dfb420ff86d66eb7ec78468b9cf60366dc8939f496322c458d8 AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/home/nonroot/python

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd \
    /uv /uvx /usr/bin/

RUN apk add --no-cache build-base git

USER nonroot

WORKDIR /home/nonroot/app

RUN uv tool install git+https://github.com/AlphaSphereDotAI/vocalizr

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:952010d4b1cf8dfb420ff86d66eb7ec78468b9cf60366dc8939f496322c458d8 AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf

RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

COPY --from=builder --chown=nonroot:nonroot --chmod=775 /home/nonroot/.local/bin /usr/bin/

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["vocalizr"]
