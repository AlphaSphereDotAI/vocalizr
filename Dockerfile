FROM cgr.dev/chainguard/wolfi-base:latest@sha256:d0142a67efcf16310e0d0f5eb75fc25d293fe04616784f6e7bc57a541d63dd9f AS builder

ARG INSTALL_SOURCE

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:94390f20a83e2de83f63b2dadcca2efab2e6798f772edab52bf545696c86bdb4 \
     /uv /uvx /usr/bin/

# skipcq: DOK-DL3018
RUN apk add --no-cache build-base git

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install "${INSTALL_SOURCE}"

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:d0142a67efcf16310e0d0f5eb75fc25d293fe04616784f6e7bc57a541d63dd9f AS production

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
