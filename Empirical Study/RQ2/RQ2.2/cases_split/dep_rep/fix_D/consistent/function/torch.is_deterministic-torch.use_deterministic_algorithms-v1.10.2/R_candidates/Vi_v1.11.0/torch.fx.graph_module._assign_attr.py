def _assign_attr(from_obj: Any, to_module: torch.nn.Module, target: str):
    *prefix, field = target.split('.')
    for item in prefix:
        t = getattr(to_module, item, None)

        if t is None:
            t = torch.nn.Module()
            setattr(to_module, item, t)
        to_module = t

    # If it is a tensor and not a parameter attribute of a module, it should be a named buffer.
    # So, we register it as a named buffer in the target module.
    if isinstance(from_obj, torch.Tensor) and not isinstance(from_obj, torch.nn.Parameter):
        to_module.register_buffer(field, from_obj)
    else:
        setattr(to_module, field, from_obj)
