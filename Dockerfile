FROM docker.io/rust:slim AS build

## cargo package name: customize here or provide via --build-arg
ARG pkg=voice_generator

WORKDIR /build

COPY . .

RUN --mount=type=cache,target=/build/target \
    --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    set -eux; \
    cargo build --release; \
    objcopy --compress-debug-sections target/release/$pkg ./main


FROM docker.io/debian:stable-slim

WORKDIR /app

## copy the main binary
COPY --from=build /build/main ./

ADD https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-en-v0_19.tar.bz2 ./kokoro-en-v0_19.tar.bz2
RUN tar xf kokoro-en-v0_19.tar.bz2 && \
    rm kokoro-en-v0_19.tar.bz2

## copy runtime assets which may or may not exist
COPY --from=build /build/Rocket.tom[l] ./static
COPY --from=build /build/stati[c] ./static
COPY --from=build /build/template[s] ./templates

## ensure the container listens globally on port 8080
ENV ROCKET_ADDRESS=0.0.0.0 \
    ROCKET_PORT=8080

CMD ./main