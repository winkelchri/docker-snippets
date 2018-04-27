#!/usr/bin/env bash

# Stops the maybe running container and start it again

HOSTNAME=""
BASE_PATH=""
CONTAINER_NAME=""
CONTAINER_IMAGE=""

RUNNING_CONTAINER=$(docker ps -a --filter name=$CONTAINER_NAME -q)

# Stops the running container
if [[ ! -z $RUNNING_CONTAINER ]]; then
        echo "Stop running container: $RUNNING_CONTAINER ..."
        docker rm -f $RUNNING_CONTAINER
        echo "done"
fi

# Consider port mapping ...
#        --publish 30080:30080 \
#        --publish 30443:443 \
#        --publish 30022:22 \


# Run the container again ...
docker run --detach --name $CONTAINER_NAME \
        --hostname "$HOSTNAME" \
        --volume $BASE_PATH/config:/etc \
        --volume $BASE_PATH/logs:/var/log \
        --volume $BASE_PATH/data:/var/opt \
        $CONTAINER_IMAGE
