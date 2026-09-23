def assert_and_get_unique_device(module: torch.nn.Module) -> Any:
    """
    Returns the unique device for a module, or None if no device is found.
    Throws an error if multiple devices are detected.
    """
    devices = {p.device for p in module.parameters()} | \
        {p.device for p in module.buffers()}
    assert len(devices) <= 1, (
        "prepare only works with cpu or single-device CUDA modules, "
        "but got devices {}".format(devices)
    )
    device = next(iter(devices)) if len(devices) > 0 else None
    return device
