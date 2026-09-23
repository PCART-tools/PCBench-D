def _maybe_fake_prop_ignore_unbacked(fn, args):
    with ExitStack() as ctx_stack:
        if (fake_mode := detect_fake_mode(args)) is not None:
            ctx_stack.enter_context(fake_mode)
            if fake_mode.shape_env is not None:
                ctx_stack.enter_context(
                    fake_mode.shape_env.ignore_fresh_unbacked_symbols()
                )
        return fn(*args)
