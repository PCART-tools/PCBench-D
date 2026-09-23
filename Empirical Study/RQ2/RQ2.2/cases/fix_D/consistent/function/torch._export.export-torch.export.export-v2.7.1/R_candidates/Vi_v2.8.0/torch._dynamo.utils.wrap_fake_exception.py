def wrap_fake_exception(fn):
    try:
        return fn()
    except UnsupportedFakeTensorException as e:
        from .exc import unimplemented_v2

        msg = f"Encountered exception ({e.reason}) during fake tensor propagation."
        log.warning(msg)
        unimplemented_v2(
            gb_type="Fake tensor propagation exception",
            context=str(e.reason),
            explanation=msg,
            hints=[],
            from_exc=e,
        )
