FROM ubuntu:jammy

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    software-properties-common \
    python3.10 \
    python3-pip

COPY /requirements.txt /

RUN --mount=type=cache,target=/var/cache/pip,sharing=locked \
    pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt

WORKDIR /opt/imt-backend
COPY /backend /opt/imt-backend

ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["main:app"]
