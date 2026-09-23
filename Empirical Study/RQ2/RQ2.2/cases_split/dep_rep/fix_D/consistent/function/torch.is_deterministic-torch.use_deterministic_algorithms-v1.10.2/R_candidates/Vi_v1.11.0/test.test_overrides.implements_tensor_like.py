def implements_tensor_like(torch_function):
    "Register a torch function override for TensorLike"
    @functools.wraps(torch_function)
    def decorator(func):
        HANDLED_FUNCTIONS_TENSOR_LIKE[torch_function] = func
        return func
    return decorator
