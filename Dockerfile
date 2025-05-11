FROM python:3.13-slim-bookworm

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_FROZEN=1 \
    GRADIO_SERVER_PORT=8080

RUN groupadd vocalizr && \
    useradd --gid vocalizr --shell /bin/bash --create-home vocalizr

# # skipcq: DOK-DL3008
# RUN apt-get update && \
#     apt-get install -qq -y --no-install-recommends espeak-ng && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv tool install huggingface-hub[cli]; \
    huggingface-cli download --quiet hexgrad/Kokoro-82M; \
    uv tool uninstall huggingface-hub

WORKDIR /home/vocalizr/app

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=README.md,target=README.md \
    --mount=type=bind,source=src,target=/home/vocalizr/app/src \
    uv export --no-hashes --no-editable --no-dev --quiet -o requirements.txt; \
    uv pip install --system -r requirements.txt

COPY --chown=vocalizr:vocalizr /src /home/vocalizr/app

USER vocalizr

EXPOSE ${GRADIO_SERVER_PORT}

ENTRYPOINT [  ]

CMD ["python", "vocalizr"]
