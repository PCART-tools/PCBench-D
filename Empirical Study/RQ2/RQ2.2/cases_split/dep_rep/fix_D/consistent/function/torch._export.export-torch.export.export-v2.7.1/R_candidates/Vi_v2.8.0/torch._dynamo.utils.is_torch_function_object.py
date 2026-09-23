def is_torch_function_object(value):
    return hasattr(value, "__torch_function__")
