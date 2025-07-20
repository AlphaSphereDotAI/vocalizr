FROM cgr.dev/chainguard/wolfi-base:latest@sha256:c4136cf075c3eccea5cb7467148ad3934753d7b47e29f78963c2f056aba19643 AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_INSTALL_DIR=/home/nonroot/python

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd \
    /uv /uvx /usr/bin/

RUN apk add --no-cache build-base

USER nonroot

WORKDIR /home/nonroot/app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --no-install-project --no-dev --locked --no-editable

COPY . /home/nonroot/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --locked --no-editable

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:c4136cf075c3eccea5cb7467148ad3934753d7b47e29f78963c2f056aba19643 AS production

ENV GRADIO_SERVER_PORT=7860 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    HF_HOME=/home/nonroot/hf

RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

COPY --from=builder --chown=nonroot:nonroot --chmod=555 /home/nonroot/python /home/nonroot/python

COPY --from=builder --chown=nonroot:nonroot --chmod=775 /home/nonroot/app/.venv /home/nonroot/app/.venv

EXPOSE ${GRADIO_SERVER_PORT}

CMD ["/home/nonroot/app/.venv/bin/vocalizr"]
