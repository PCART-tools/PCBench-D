def gen_docker_image(container_type):
    return (
        "/".join([AWS_DOCKER_HOST, "pytorch", container_type]),
        f"docker-{container_type}",
    )
