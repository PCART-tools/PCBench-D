def get_workflow_jobs(only_slow_gradcheck=False):
    """Generates a list of docker image build definitions"""
    ret = []
    for image_name in IMAGE_NAMES:
        if only_slow_gradcheck and image_name is not SLOW_GRADCHECK_IMAGE_NAME:
            continue

        parameters = OrderedDict({
            "name": quote(f"docker-{image_name}"),
            "image_name": quote(image_name),
        })
        if image_name == "pytorch-linux-xenial-py3.6-gcc5.4":
            # pushing documentation on tags requires CircleCI to also
            # build all the dependencies on tags, including this docker image
            parameters['filters'] = gen_filter_dict(branches_list=r"/.*/",
                                                    tags_list=RC_PATTERN)
        ret.append(OrderedDict(
            {
                "docker_build_job": parameters
            }
        ))
    return ret
