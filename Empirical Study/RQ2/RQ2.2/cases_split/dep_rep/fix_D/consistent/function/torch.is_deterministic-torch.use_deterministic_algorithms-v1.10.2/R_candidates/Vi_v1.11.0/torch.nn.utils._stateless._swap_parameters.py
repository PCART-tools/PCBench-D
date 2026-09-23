def _swap_parameters(module, tensor_name: str, tensor: Tensor) -> None:
    # Changes the module class to get a new __getattr__ dunder method
    # that looks for the reparametrized tensor
    if hasattr(module, "_functional_parameters"):
        module._functional_parameters[tensor_name] = tensor
    else:
        module._functional_parameters = {}
        module._functional_parameters[tensor_name] = tensor
        _change_class(module)
