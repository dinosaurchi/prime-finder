# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.7

ARG CLIENT_SERVICE_DIR
ARG PROTO_DIR

WORKDIR /usr/src
COPY $CLIENT_SERVICE_DIR /usr/src
COPY $PROTO_DIR/python /usr/proto

# setup the environment
RUN \
	# =========================
	# Instal the environment
	# =========================
	pip install -e . \
	pip install -e ../proto \
	# -------------------------
	# =========================
	# Run unittest
	# =========================
	&& python tests/run_test.py
	# -------------------------