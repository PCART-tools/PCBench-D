def is_compile_supported(device_type):
    from .eval_frame import is_dynamo_supported

    compile_supported = is_dynamo_supported()
    if device_type == "cpu":
        pass
    elif device_type in ["cuda", "xpu"] and compile_supported:
        compile_supported = has_triton()
    else:
        compile_supported = False
    return compile_supported
