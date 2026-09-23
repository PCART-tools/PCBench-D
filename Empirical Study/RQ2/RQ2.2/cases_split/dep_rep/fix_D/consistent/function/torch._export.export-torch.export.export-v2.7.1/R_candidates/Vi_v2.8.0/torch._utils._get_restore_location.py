def _get_restore_location(device):
    """Return the map_location location.

    Used for rebuild functions where the tensor device is distinct from the storage
    """

    map_location = torch.serialization._serialization_tls.map_location
    if map_location is None:
        return device
    else:
        if isinstance(map_location, dict):
            return map_location.get(device, device)
        elif isinstance(map_location, (str, torch.device)):
            return map_location
        else:
            assert callable(map_location)
            raise RuntimeError(
                "Callable map_location not supported with _rebuild_wrapper_subclass "
                "or _rebuild_device_tensor_from_numpy"
            )
