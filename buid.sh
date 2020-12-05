source .env

COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build \
	--build-arg CLIENT_SERVICE_DIR="$CLIENT_SERVICE_DIR" \
	--build-arg CORE_SERVICE_DIR="$CORE_SERVICE_DIR" \
	--build-arg PROTO_DIR="$PROTO_DIR"