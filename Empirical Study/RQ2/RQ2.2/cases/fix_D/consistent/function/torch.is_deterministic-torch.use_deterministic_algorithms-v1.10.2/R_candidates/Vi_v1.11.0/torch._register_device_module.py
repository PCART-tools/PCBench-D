def _register_device_module(device_type, module):
    r"""Register an external runtime module of the specific :attr:`device_type`
    supported by torch.

    After the :attr:`module` is registered correctly, the user can refer
    the external runtime module as part of torch with attribute torch.xxx.
    """
    # Make sure the device_type represent a supported device type for torch.
    device_type = torch.device(device_type).type
    m = sys.modules[__name__]
    if hasattr(m, device_type):
        raise RuntimeError("The runtime module of '{}' has already "
                           "been registered with '{}'".format(device_type, getattr(m, device_type)))
    setattr(m, device_type, module)
