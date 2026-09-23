def disable_translation_validation_if_dynamic_shapes(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if torch._dynamo.config.dynamic_shapes:
            # Turning TV off due to high latency on dynamic shapes.
            torch.fx.experimental._config.translation_validation = False
        return fn(*args, **kwargs)
    return wrapper
