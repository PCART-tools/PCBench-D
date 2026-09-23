def synchronize(device: Optional[_device_t] = None) -> None:
    r"""Waits for all jobs in all streams on a MTIA device to complete."""
    with torch.mtia.device(device):
        return torch._C._mtia_deviceSynchronize()
