def update(op, device_name, version, key, value):
    """Update the db of op parameters."""
    # skip storing possible optimization failures:
    if not value:
        warnings.warn(
            f"skipping empty value for {op}: {device_name=} {version=} {key=}"
        )
        return
    if (op, device_name, version) in _operation_device_version_data:
        if _operation_device_version_data[op, device_name, version].get(key) == value:
            return
        _operation_device_version_data[op, device_name, version][key] = value
    else:
        _operation_device_version_data[op, device_name, version] = {key: value}
