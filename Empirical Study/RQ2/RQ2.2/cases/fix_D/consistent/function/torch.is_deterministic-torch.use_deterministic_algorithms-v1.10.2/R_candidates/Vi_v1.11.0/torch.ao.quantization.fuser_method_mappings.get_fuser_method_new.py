def get_fuser_method_new(
        op_pattern: Pattern,
        fuser_method_mapping: Optional[Dict[Pattern, Union[nn.Sequential, Callable]]] = None):
    """ This will be made defult after we deparate the get_fuser_method
    Would like to implement this first and have a separate PR for deprecation
    """
    if fuser_method_mapping is None:
        fuser_method_mapping = DEFAULT_PATTERN_TO_FUSER_METHOD

    fuser_method = fuser_method_mapping.get(op_pattern, None)
    assert fuser_method is not None, "did not find fuser method for: {} ".format(op_pattern)
    return fuser_method
