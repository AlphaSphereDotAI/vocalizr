FROM cgr.dev/chainguard/wolfi-base:latest@sha256:c4136cf075c3eccea5cb7467148ad3934753d7b47e29f78963c2f056aba19643 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd \
    /uv /uvx /usr/bin/

RUN apk add --no-cache build-base git

USER nonroot

RUN uv tool install git+https://github.com/AlphaSphereDotAI/vocalizr

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:c4136cf075c3eccea5cb7467148ad3934753d7b47e29f78963c2f056aba19643 AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf

RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

RUN mkdir -p /home/nonroot/bin
COPY --from=builder /home/nonroot/.local/bin/vocalizr /home/nonroot/bin/
ENV PATH="/home/nonroot/bin:${PATH}"

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["vocalizr"]
