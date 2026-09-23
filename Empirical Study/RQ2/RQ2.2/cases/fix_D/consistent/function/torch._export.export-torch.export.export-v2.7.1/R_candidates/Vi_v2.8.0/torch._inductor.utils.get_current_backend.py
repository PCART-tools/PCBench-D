def get_current_backend() -> str:
    from torch._inductor.virtualized import V

    device_str = V.graph.get_current_device_or_throw().type
    if device_str == "cpu":
        return config.cpu_backend
    elif device_str == "mps":
        return "mps"
    else:
        return config.cuda_backend
