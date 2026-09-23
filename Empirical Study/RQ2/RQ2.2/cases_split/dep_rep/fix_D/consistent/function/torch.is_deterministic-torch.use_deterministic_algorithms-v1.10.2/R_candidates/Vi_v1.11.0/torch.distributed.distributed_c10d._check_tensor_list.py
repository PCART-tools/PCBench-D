def _check_tensor_list(param, param_name):
    """
    Helper to check that the parameter ``param_name`` is a list of tensors.
    """
    if not isinstance(param, list) or not all(
        isinstance(p, torch.Tensor) for p in param
    ):
        raise RuntimeError(
            "Invalid function argument. Expected parameter `{}` "
            "to be of type List[torch.Tensor].".format(param_name)
        )
