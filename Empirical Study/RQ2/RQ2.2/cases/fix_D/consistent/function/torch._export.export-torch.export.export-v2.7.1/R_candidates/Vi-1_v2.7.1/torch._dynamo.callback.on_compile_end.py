def on_compile_end(callback: Callable[[], None]) -> Callable[[], None]:
    """
    Decorator to register a callback function for the end of the compilation.
    """
    callback_handler.register_end_callback(callback)
    return callback
