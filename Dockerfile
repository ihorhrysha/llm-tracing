# https://github.com/open-telemetry/opentelemetry-demo/blob/main/src/recommendationservice/Dockerfile

FROM python:3.12-slim-bookworm as base

#
# Fetch requirements
#
FROM base as builder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY ./src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --prefix="/reqs" -r requirements.txt

#
# Runtime
#
FROM base as runtime
WORKDIR /usr/src/app/
COPY --from=builder /reqs /usr/local
COPY ./src/ ./


# This doesn't work quite well
# RUN opentelemetry-bootstrap -a install

# EXPOSE 8080
ENTRYPOINT ["flask", "--app", "app_flask.py", "run", "-p", "8080", "-h", "0.0.0.0"]
