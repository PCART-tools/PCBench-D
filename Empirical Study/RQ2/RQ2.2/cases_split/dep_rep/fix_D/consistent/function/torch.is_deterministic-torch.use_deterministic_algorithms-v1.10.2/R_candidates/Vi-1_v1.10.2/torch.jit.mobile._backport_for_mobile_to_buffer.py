def _backport_for_mobile_to_buffer(f_input, to_version):
    r"""
    Args:
        f_input: a file-like object (has to implement read, readline, tell, and seek),
            or a string containing a file name

    """
    if isinstance(f_input, str):
        if not os.path.exists(f_input):
            raise ValueError(f"The provided filename {f_input} does not exist")
        if os.path.isdir(f_input):
            raise ValueError(f"The provided filename {f_input} is a directory")

    if (isinstance(f_input, str) or isinstance(f_input, pathlib.Path)):
        return torch._C._backport_for_mobile_to_buffer(str(f_input), to_version)
    else:
        return torch._C._backport_for_mobile_from_buffer_to_buffer(f_input.read(), to_version)
