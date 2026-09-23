def _callback_from_stance(callback):
    if _stance.stance == "default":
        # force_backend
        if _stance.backend is not None and callback not in (False, None):
            callback = _create_wrapped_callback(get_compiler_fn(_stance.backend))

        return callback
    elif _stance.stance == "eager_then_compile":
        if callback not in (False, None):
            return _create_delayed_compile_callback(callback, _stance.stance)
        return callback
    elif _stance.stance == "aot_eager_then_compile":
        if callback not in (False, None):
            return _create_delayed_compile_callback(callback, _stance.stance)
        return callback
    elif _stance.stance == "force_eager":
        # disable
        return None
    elif _stance.stance == "eager_on_recompile":
        # run mode
        return False
    elif _stance.stance == "fail_on_recompile":
        if callback in (False, None):
            return callback

        def fail_callback(*args, **kwargs):
            raise RuntimeError(
                "Detected recompile when torch.compile stance is 'fail_on_recompile'"
            )

        # to prevent cache miss due to different callback
        fail_callback._torchdynamo_orig_callable = callback  # type: ignore[attr-defined]

        return fail_callback
    else:
        raise RuntimeError(f"invalid torch.compile stance '{_stance}'")
