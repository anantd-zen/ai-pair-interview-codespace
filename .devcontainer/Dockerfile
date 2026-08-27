FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# The base image currently carries a Yarn APT source whose rotated signing key
# breaks apt-get update inside later devcontainer features. Node is installed
# through the official Node feature, so this legacy source is unnecessary.
RUN rm -f /etc/apt/sources.list.d/yarn.list

