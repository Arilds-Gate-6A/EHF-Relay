FROM python:3.13.3-slim-bookworm AS build

RUN mkdir /usr/src/ehf-relay

WORKDIR /usr/src/ehf-relay

RUN apt update \
    && apt install -y python3-poetry

COPY pyproject.toml .
COPY ehf_relay ./ehf_relay

RUN poetry build

FROM python:3.13.3-slim-bookworm

ARG VERSION="0.1.0"

ARG WHEEL="ehf_relay-${VERSION}-py3-none-any.whl"

RUN adduser ehfrelay

USER ehfrelay

COPY --from=build --chmod=+x /usr/src/ehf-relay/dist/${WHEEL} /home/ehfrelay

RUN echo ${WHEEL}

RUN pip install /home/ehfrelay/${WHEEL}

CMD ["python", "-m", "ehf_relay"]
