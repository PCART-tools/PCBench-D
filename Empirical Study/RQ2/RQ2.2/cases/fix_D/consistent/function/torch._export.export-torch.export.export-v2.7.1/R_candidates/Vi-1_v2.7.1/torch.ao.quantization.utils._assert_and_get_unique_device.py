def _assert_and_get_unique_device(module: torch.nn.Module) -> Any:
    """
    Returns the unique device for a module, or None if no device is found.
    Throws an error if multiple devices are detected.
    """
    devices = {p.device for p in module.parameters()} | {
        p.device for p in module.buffers()
    }
    """
    As a temp workaround for AIMP HHC publish we added CPU check.remove it later. T163614564
    """
    if {torch.device("cpu"), torch.device("meta")} == devices:
        warnings.warn(
            "Both 'meta' and 'cpu' are present in the list of devices. Module can have one device. We Select 'cpu'."
        )
        devices = {torch.device("cpu")}
    ""
    assert len(devices) <= 1, (
        "prepare only works with cpu or single-device CUDA modules, "
        f"but got devices {devices}"
    )
    device = next(iter(devices)) if len(devices) > 0 else None
    return device
