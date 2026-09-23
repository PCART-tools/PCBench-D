def default_restore_location(storage, location):
    for _, _, fn in _package_registry:
        result = fn(storage, location)
        if result is not None:
            return result
    raise RuntimeError("don't know how to restore data location of "
                       + torch.typename(storage) + " (tagged with "
                       + location + ")")
