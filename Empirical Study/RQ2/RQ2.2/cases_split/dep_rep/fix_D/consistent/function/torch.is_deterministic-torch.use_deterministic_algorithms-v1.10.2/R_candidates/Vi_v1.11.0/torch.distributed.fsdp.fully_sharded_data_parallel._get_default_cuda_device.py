def _get_default_cuda_device(module: nn.Module) -> torch.device:
    """Try to infer CUDA device from module parameters."""
    try:
        compute_device = next(module.parameters()).device
        if compute_device.type == "cuda":
            return compute_device
    # e.g., if module does not have parameters, it will throw StopIteration,
    # in this case, instead of raising exception, return cuda device.
    except StopIteration:
        pass
    # Fall back to current CUDA device
    return torch.device("cuda")
