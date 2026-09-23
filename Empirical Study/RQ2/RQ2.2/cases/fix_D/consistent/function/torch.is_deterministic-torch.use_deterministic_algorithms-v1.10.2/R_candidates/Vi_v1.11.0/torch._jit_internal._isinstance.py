def _isinstance(obj, target_type) -> bool:
    if isinstance(target_type, collections.abc.Container):
        if not isinstance(target_type, tuple):
            raise RuntimeError("The second argument to "
                               "`torch.jit.isinstance` must be a type "
                               "or a tuple of types")
        for t_type in target_type:
            if _isinstance(obj, t_type):
                return True
        return False

    origin_type = get_origin(target_type)
    if origin_type:
        return container_checker(obj, target_type)

    # Check to handle weird python type behaviors
    # 1. python 3.6 returns None for origin of containers without
    #    contained type (intead of returning outer container type)
    # 2. non-typed optional origin returns as none instead
    #    of as optional in 3.6-3.8
    check_args_exist(target_type)

    # handle non-containers
    return isinstance(obj, target_type)
