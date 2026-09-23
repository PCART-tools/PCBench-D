def get_engine():
    if tensor_engine is None:
        raise ValueError("use of get_engine, before calling set_engine_mode is illegal")
    return tensor_engine
