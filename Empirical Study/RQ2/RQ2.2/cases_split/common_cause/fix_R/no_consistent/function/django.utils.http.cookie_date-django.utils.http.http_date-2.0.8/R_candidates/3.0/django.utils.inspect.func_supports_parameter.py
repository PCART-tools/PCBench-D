def func_supports_parameter(func, parameter):
    return parameter in inspect.signature(func).parameters
