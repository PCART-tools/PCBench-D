def _get_decoding_default_config(key) -> tuple[int, int, int]:
    dtype = key.get_dtype()
    head_dim = key.get_size()[-1]
    sm_version = torch.cuda.get_device_capability()
    default_config = (64, 2, 1)
    if sm_version >= (9, 0):
        if head_dim > 128 and dtype == torch.float32:
            return default_config
        if torch.version.hip is None:
            return (64, 2, 3)
        else:
            return (64, 2, 1)
    return default_config
