def _split_module(modules: nn.Sequential) -> Tuple[List[nn.Sequential], List[torch.device]]:
    partitions = []
    devices = []

    current_partition = []
    current_device = None
    for name, module in modules.named_children():
        if isinstance(module, WithDevice):
            # Process device override and move module to appropriate device.
            device = module.device
            module = module.module
            module.to(device)
        else:
            device = _retrieve_device(module)
        if current_device is not None and (current_device != device or device.type == 'cpu'):
            partitions.append(_assemble_partition(current_partition))
            devices.append(current_device)
            current_partition = []
        current_device = device
        current_partition.append(module)

    if current_device is not None:
        partitions.append(_assemble_partition(current_partition))
        devices.append(current_device)

    partitions = cast(List[nn.Sequential], nn.ModuleList(partitions))

    return partitions, devices
