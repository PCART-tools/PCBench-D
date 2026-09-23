def gen_mobile_docker(specifier):
    container_type = "pytorch-linux-xenial-py3-clang5-" + specifier
    return gen_docker_image(container_type)
