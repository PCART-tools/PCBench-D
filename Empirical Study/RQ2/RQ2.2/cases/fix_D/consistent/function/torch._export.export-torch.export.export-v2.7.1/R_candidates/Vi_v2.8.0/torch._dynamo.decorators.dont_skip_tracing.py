def dont_skip_tracing(fn=None):
    """
    Context manager/decorator to trace into functions intentionally marked by developers to be skipped
    when tracing.

    This decorator will also apply to recursively invoked functions.
    """
    ctx = patch_dynamo_config(dont_skip_tracing=True)
    if fn:
        return ctx(fn)
    return ctx
