def device_count() -> int:
    r"""Return the number of MTIA devices available."""
    # TODO: Update _accelerator_hooks_device_count to abstract a MTIA device count API
    return torch._C._mtia_getDeviceCount()
