def construct_dict(cls, /, *args, **kwargs):
    dst = cls.__new__(cls)

    if args:
        src = args[0]

        # Ensure that the overridden __iter__ method is invoked
        if isinstance(src, (dict, MutableMapping, types.MappingProxyType)):
            for key in src:
                # This will inline the __getitem__ of the src object
                dst[key] = src[key]
        else:
            # likely a sequence like tuple of pairs
            for key, value in src:
                dst[key] = value

    if kwargs:
        for key in kwargs:
            dst[key] = kwargs[key]

    return dst
