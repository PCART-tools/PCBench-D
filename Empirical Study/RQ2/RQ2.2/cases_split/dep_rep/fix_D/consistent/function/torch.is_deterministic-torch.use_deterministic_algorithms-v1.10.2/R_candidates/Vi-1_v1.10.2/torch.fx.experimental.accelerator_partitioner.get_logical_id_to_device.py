def get_logical_id_to_device(devices: List[Device]) -> Dict[int, Device]:
    """Get a mapping from device logical ID to Device object."""
    logical_id_to_device: Dict[int, Device] = {}
    for d in devices:
        logical_id_to_device[d.logical_id] = d
    return logical_id_to_device
