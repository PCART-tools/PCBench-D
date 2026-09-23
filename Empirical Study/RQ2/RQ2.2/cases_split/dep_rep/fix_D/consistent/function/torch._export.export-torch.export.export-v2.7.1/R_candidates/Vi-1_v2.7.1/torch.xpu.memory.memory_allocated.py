def memory_allocated(device: _device_t = None) -> int:
    r"""Return the current GPU memory occupied by tensors in bytes for a given device.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        This is likely less than the amount shown in `xpu-smi` since some
        unused memory can be held by the caching allocator and some context
        needs to be created on GPU.
    """
    return memory_stats(device=device).get("allocated_bytes.all.current", 0)
