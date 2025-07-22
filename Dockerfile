FROM cgr.dev/chainguard/wolfi-base:latest@sha256:7bc3ad6c31262f9556bd2dff1479f7f4ae9842c5fc765618be795bc85a96c97e AS builder

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5754244acb75f7c7dcc40f6bac02101fe3d0cae6d536e776de62e392a4753f3a \
     /uv /uvx /usr/bin/

RUN apk add --no-cache build-base git

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install git+https://github.com/AlphaSphereDotAI/vocalizr

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:7bc3ad6c31262f9556bd2dff1479f7f4ae9842c5fc765618be795bc85a96c97e AS production

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
