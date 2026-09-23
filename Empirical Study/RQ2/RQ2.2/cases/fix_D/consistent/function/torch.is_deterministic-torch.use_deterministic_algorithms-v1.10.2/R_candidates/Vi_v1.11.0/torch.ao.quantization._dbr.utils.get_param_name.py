def get_param_name(module: torch.nn.Module, arg: Any) -> Optional[str]:
    """
    Returns the name of arg with respect to the current module.
    """
    for name, param in module.named_parameters():
        if arg is param:
            return name
    return None
