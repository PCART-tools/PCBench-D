def is_available() -> bool:
    return hasattr(torch._C, "_rpc_init")
