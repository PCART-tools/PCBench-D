def set_onnx_exporting_flag(func: TCallable) -> TCallable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        global _is_onnx_exporting
        _is_onnx_exporting = True
        try:
            return func(*args, **kwargs)
        finally:
            # Ensure it resets even if an exception occurs
            _is_onnx_exporting = False

    return cast(TCallable, wrapper)
