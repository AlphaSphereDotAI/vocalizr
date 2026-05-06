FROM cgr.dev/chainguard/wolfi-base:latest@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder

ARG INSTALL_SOURCE
ARG PYTHON_VERSION

# skipcq: DOK-DL3018
RUN apk add --no-cache build-base git uv

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install "${INSTALL_SOURCE}" --python "${PYTHON_VERSION}"

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS production

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
