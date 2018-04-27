# Stops the maybe running container and start it again

import os
from subprocess import run, PIPE
from pathlib import Path

HOSTNAME = "localhost"
BASE_PATH = Path(".").absolute()
CONTAINER_NAME = "some_container_name"
CONTAINER_IMAGE = "some_container_image"
INTERACTIVE = False

PATH_MAPPING = {
    BASE_PATH / "config": "/etc",
    BASE_PATH / "logs": "/var/log",
    BASE_PATH / "data": "/var/opt"
}


def get_running_container_id(container_name):
    ''' Return the container id to the given container name.
        Returns None if there is no running container with this name.
    '''

    process = run(
        "docker ps -a --filter name={} -q".format(container_name),
        shell=True,
        stdout=PIPE
    )

    if process.stdout != b"":
        return process.stdout.decode("utf-8").strip()
    return None


def stop_container(container_id):
    ''' Stops the container of the given container id. '''

    print("Stop running container: {} ...".format(container_id))
    run("docker rm -f {}".format(container_id), shell=True, stdout=PIPE)
    print("done")


def start_container(container_name, path_mapping=None):
    ''' Start the container with the given name. '''

    def create_mapping_paths(path_mapping):
        ''' Create necessary directories for path mapping '''

        for local_path in path_mapping.keys():
            if not local_path.is_dir():
                os.makedirs(local_path.as_posix())

    def path_mapping_to_string(path_mapping):
        ''' Returns a docker command compatible string
            out of the path_mapping.
        '''

        return " ".join([
            "--volume {}:{}".format(key.as_posix(), value)
            for key, value in path_mapping.items()
        ])

    # Switch if path_mapping is present
    if path_mapping is not None:
        create_mapping_paths(path_mapping)
        path_mapping_string = path_mapping_to_string(path_mapping)
    else:
        path_mapping_string = ""

    # Create the docker command
    command = (
        'docker run --detach --name {container_name} '
        '--hostname {hostname} '
        '{path_mapping} '
        '{container_image}'
    ).format(
        container_name=container_name,
        hostname=HOSTNAME,
        path_mapping=path_mapping_string,
        container_image=CONTAINER_IMAGE
    )

    run(command, shell=True)


def main():
    container_id = get_running_container_id(CONTAINER_NAME)
    if container_id is not None:
        stop_container(container_id)
    start_container(container_name=CONTAINER_NAME, path_mapping=PATH_MAPPING)

if __name__ == '__main__':
    main()
