def node_ctor_inputs(func: LazyIrSchema) -> str:
    """
    Produce a formatted string with the arguments as passed into the constructor of a node class.
    """
    node_ctor_values = [node_ctor_arg_rvalue_string(arg) for arg in func.filtered_types()]
    return ",\n                              ".join(node_ctor_values)
