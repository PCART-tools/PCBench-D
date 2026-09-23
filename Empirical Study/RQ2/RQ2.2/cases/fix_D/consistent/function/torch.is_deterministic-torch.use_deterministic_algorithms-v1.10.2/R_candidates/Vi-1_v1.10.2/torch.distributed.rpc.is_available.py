def is_available():
    return hasattr(torch._C, "_rpc_init")
