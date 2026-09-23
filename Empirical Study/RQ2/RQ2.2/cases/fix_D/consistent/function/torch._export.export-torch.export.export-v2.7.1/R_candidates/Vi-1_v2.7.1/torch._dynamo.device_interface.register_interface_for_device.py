def register_interface_for_device(
    device: Union[str, torch.device], device_interface: type[DeviceInterface]
):
    if isinstance(device, torch.device):
        device = device.type
    device_interfaces[device] = device_interface
