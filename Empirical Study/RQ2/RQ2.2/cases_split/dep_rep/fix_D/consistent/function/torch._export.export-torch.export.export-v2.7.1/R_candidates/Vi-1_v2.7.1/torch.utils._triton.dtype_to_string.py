def dtype_to_string(dtype):
    if dtype.name.startswith("fp"):
        suffix = "float" + dtype.name[2:]
    elif dtype.name.startswith("bf"):
        suffix = "bfloat" + dtype.name[2:]
    else:
        suffix = dtype.name
    return "triton.language." + suffix
