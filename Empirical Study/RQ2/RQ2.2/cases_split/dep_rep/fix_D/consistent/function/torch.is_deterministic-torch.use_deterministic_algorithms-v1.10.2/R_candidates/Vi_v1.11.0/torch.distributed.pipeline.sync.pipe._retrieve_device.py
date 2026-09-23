def _retrieve_device(module: nn.Module) -> torch.device:
    """Validates all parameters in the Module have the same device and returns
    the appropriate device.

    Args:
        An ``nn.Module`` to process.

    Returns:
        ``torch.Device`` for the entire module.

    Raises:
        ValueError:
            If devices for ``nn.Module`` parameters are not all same.
    """

    device = None
    for parameter in module.parameters():
        if device is None:
            device = parameter.device
        elif device != parameter.device:
            raise ValueError(
                'nn.Module: {}, should have all parameters on a single device,'
                ' please use .to() to place the module on a single device'.format(module))

    return device if device is not None else torch.device("cpu")
