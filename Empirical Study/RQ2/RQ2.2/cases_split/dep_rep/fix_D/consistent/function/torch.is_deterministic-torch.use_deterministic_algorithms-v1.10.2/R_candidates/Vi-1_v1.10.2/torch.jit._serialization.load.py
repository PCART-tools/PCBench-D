def load(f, map_location=None, _extra_files=None):
    r"""
    Load a :class:`ScriptModule` or :class:`ScriptFunction` previously
    saved with :func:`torch.jit.save <torch.jit.save>`

    All previously saved modules, no matter their device, are first loaded onto CPU,
    and then are moved to the devices they were saved from. If this fails (e.g.
    because the run time system doesn't have certain devices), an exception is
    raised.

    Args:
        f: a file-like object (has to implement read, readline, tell, and seek),
            or a string containing a file name
        map_location (string or torch.device): A simplified version of
            ``map_location`` in `torch.jit.save` used to dynamically remap
            storages to an alternative set of devices.
        _extra_files (dictionary of filename to content): The extra
            filenames given in the map would be loaded and their content
            would be stored in the provided map.

    Returns:
        A :class:`ScriptModule` object.

    Example:

    .. testcode::

        import torch
        import io

        torch.jit.load('scriptmodule.pt')

        # Load ScriptModule from io.BytesIO object
        with open('scriptmodule.pt', 'rb') as f:
            buffer = io.BytesIO(f.read())

        # Load all tensors to the original device
        torch.jit.load(buffer)

        # Load all tensors onto CPU, using a device
        buffer.seek(0)
        torch.jit.load(buffer, map_location=torch.device('cpu'))

        # Load all tensors onto CPU, using a string
        buffer.seek(0)
        torch.jit.load(buffer, map_location='cpu')

        # Load with extra files.
        extra_files = {'foo.txt': ''}  # values will be replaced with data
        torch.jit.load('scriptmodule.pt', _extra_files=extra_files)
        print(extra_files['foo.txt'])

    .. testoutput::
        :hide:

        ...

    .. testcleanup::

        import os
        os.remove("scriptmodule.pt")
    """
    if isinstance(f, string_classes):
        if not os.path.exists(f):  # type: ignore[type-var]
            raise ValueError("The provided filename {} does not exist".format(f))  # type: ignore[str-bytes-safe]
        if os.path.isdir(f):
            raise ValueError("The provided filename {} is a directory".format(f))  # type: ignore[str-bytes-safe]

    map_location = validate_map_location(map_location)
    if _extra_files is None:
        _extra_files = {}

    cu = torch._C.CompilationUnit()
    if isinstance(f, str) or isinstance(f, pathlib.Path):
        cpp_module = torch._C.import_ir_module(cu, str(f), map_location, _extra_files)
    else:
        cpp_module = torch._C.import_ir_module_from_buffer(
            cu, f.read(), map_location, _extra_files
        )

    # TODO: Pretty sure this approach loses ConstSequential status and such
    return wrap_cpp_module(cpp_module)
