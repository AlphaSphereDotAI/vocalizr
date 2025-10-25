FROM cgr.dev/chainguard/wolfi-base:latest@sha256:0d1673dd55e8b7535fea5191c8337f0c18f46d55ed9020b9dcc1a2e17c550680 AS builder

ARG INSTALL_SOURCE
ARG PYTHON_VERSION

# skipcq: DOK-DL3018
RUN apk add --no-cache build-base git uv

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install "${INSTALL_SOURCE}" --python "${PYTHON_VERSION}"

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:0d1673dd55e8b7535fea5191c8337f0c18f46d55ed9020b9dcc1a2e17c550680 AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf \
    PATH=/home/nonroot/.local/bin:$PATH

# skipcq: DOK-DL3018
RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

COPY --from=builder --chown=nonroot:nonroot --chmod=755 /home/nonroot/.local/ /home/nonroot/.local/

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["vocalizr"]
