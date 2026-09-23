def load(f, map_location=None, _extra_files=None, _restore_shapes=False):
    r"""
    Load a :class:`ScriptModule` or :class:`ScriptFunction` previously saved with :func:`torch.jit.save <torch.jit.save>`.

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
        _restore_shapes (bool): Whether or not to retrace the module on load using stored inputs

    Returns:
        A :class:`ScriptModule` object.

    .. warning::
        It is possible to construct malicious pickle data which will execute arbitrary code
        during func:`torch.jit.load`. Never load data that could have come from an untrusted
        source, or that could have been tampered with. **Only load data you trust**.

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
    if isinstance(f, (str, os.PathLike)):
        if not os.path.exists(f):
            raise ValueError(f"The provided filename {f} does not exist")
        if os.path.isdir(f):
            raise ValueError(f"The provided filename {f} is a directory")

    map_location = validate_map_location(map_location)
    if _extra_files is None:
        _extra_files = {}

    cu = torch._C.CompilationUnit()
    if isinstance(f, (str, os.PathLike)):
        cpp_module = torch._C.import_ir_module(
            cu, os.fspath(f), map_location, _extra_files, _restore_shapes
        )  # type: ignore[call-arg]
    else:
        cpp_module = torch._C.import_ir_module_from_buffer(
            cu, f.read(), map_location, _extra_files, _restore_shapes
        )  # type: ignore[call-arg]

    # TODO: Pretty sure this approach loses ConstSequential status and such
    ret = wrap_cpp_module(cpp_module)
    log_torchscript_usage("load", model_id=_get_model_id(ret))
    return ret
