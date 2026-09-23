def _dtype_is_fp(type_value):
    if type_value:
        return (type_value == torch.float16) or (type_value == torch.float32) or (type_value == torch.float64)
    return False
