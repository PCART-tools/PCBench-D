def _check_single_tensor(param, param_name):
    """
    Helper to check that the parameter ``param_name`` is a single tensor.
    """
    if not isinstance(param, torch.Tensor):
        raise RuntimeError(
            "Invalid function argument. Expected parameter `{}` "
            "to be of type torch.Tensor.".format(param_name)
        )
