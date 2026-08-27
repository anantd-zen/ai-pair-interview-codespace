FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/

ARG DUCKDB_VERSION=1.5.5
ARG DUCKDB_SHA256=c61f21485e6e41d3a0c28ce9904ea18346309cf427b4cf9479bc3564348dc885

# The base image currently carries a legacy Yarn APT source whose rotated key
# can break apt-get update. Node is installed by the devcontainer feature.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gzip \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL \
       "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-amd64.gz" \
       -o /tmp/duckdb.gz \
    && echo "${DUCKDB_SHA256}  /tmp/duckdb.gz" | sha256sum --check --strict \
    && gzip -dc /tmp/duckdb.gz > /usr/local/bin/duckdb \
    && chmod 0755 /usr/local/bin/duckdb \
    && rm /tmp/duckdb.gz

