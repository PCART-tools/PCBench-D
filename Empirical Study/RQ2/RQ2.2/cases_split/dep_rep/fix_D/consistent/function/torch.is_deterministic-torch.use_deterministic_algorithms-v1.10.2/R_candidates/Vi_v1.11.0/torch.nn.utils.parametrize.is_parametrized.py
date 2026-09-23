def is_parametrized(module: Module, tensor_name: Optional[str] = None) -> bool:
    r"""Returns ``True`` if module has an active parametrization.

    If the argument :attr:`tensor_name` is specified, returns ``True`` if
    ``module[tensor_name]`` is parametrized.

    Args:
        module (nn.Module): module to query
        name (str, optional): attribute in the module to query
            Default: ``None``
    """
    parametrizations = getattr(module, "parametrizations", None)
    if parametrizations is None or not isinstance(parametrizations, ModuleDict):
        return False
    if tensor_name is None:
        # Check that there is at least one parametrized buffer or Parameter
        return len(parametrizations) > 0
    else:
        return tensor_name in parametrizations
