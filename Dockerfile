FROM cgr.dev/chainguard/wolfi-base:latest@sha256:ae238a181d95804645919b2671d50ae77477efbfb299544491346e2911125aaf AS builder

ARG INSTALL_SOURCE
ARG PYTHON_VERSION

# skipcq: DOK-DL3018
RUN apk add --no-cache build-base git uv

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install "${INSTALL_SOURCE}" --python "${PYTHON_VERSION}"

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:ae238a181d95804645919b2671d50ae77477efbfb299544491346e2911125aaf AS production

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
