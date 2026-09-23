def _load_local(hubconf_dir, model, *args, **kwargs):
    r"""
    Load a model from a local directory with a ``hubconf.py``.

    Args:
        hubconf_dir (string): path to a local directory that contains a
            ``hubconf.py``.
        model (string): name of an entrypoint defined in the directory's
            ``hubconf.py``.
        *args (optional): the corresponding args for callable ``model``.
        **kwargs (optional): the corresponding kwargs for callable ``model``.

    Returns:
        a single model with corresponding pretrained weights.

    Example:
        >>> path = '/some/local/path/pytorch/vision'
        >>> model = _load_local(path, 'resnet50', pretrained=True)
    """
    sys.path.insert(0, hubconf_dir)

    hubconf_path = os.path.join(hubconf_dir, MODULE_HUBCONF)
    hub_module = import_module(MODULE_HUBCONF, hubconf_path)

    entry = _load_entry_from_hubconf(hub_module, model)
    model = entry(*args, **kwargs)

    sys.path.remove(hubconf_dir)

    return model
