def op_needs_quantization(op: Callable) -> bool:
    if op in functions_supported_by_quantization:
        return True
    elif type(op) in module_types_supported_by_quantization:
        return True
    else:
        return False
