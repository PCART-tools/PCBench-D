def device_from_inputs(example_inputs) -> torch.device:
    for x in example_inputs:
        if hasattr(x, "device"):
            return x.device
