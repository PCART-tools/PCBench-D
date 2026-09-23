def _script_if_tracing(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not is_tracing():
            # Not tracing, don't do anything
            return fn(*args, **kwargs)

        compiled_fn = script(wrapper.__original_fn)  # type: ignore[attr-defined]
        return compiled_fn(*args, **kwargs)

    wrapper.__original_fn = fn  # type: ignore[attr-defined]
    wrapper.__script_if_tracing_wrapper = True  # type: ignore[attr-defined]

    return wrapper
