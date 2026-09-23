def is_cpu(x: Union[IRNode, torch.device, None, str]) -> bool:
    return get_device_type(x) == "cpu"
