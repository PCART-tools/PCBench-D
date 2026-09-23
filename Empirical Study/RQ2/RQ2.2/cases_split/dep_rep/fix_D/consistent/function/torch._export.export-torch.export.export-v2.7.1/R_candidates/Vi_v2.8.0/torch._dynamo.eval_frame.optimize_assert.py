def optimize_assert(*args, **kwargs):
    if "rebuild_ctx" in kwargs and kwargs["rebuild_ctx"] is not None:
        # called from optimize
        rebuild_ctx = kwargs["rebuild_ctx"]
        del kwargs["rebuild_ctx"]
    else:

        def rebuild_ctx():
            return optimize_assert(*args, **kwargs)

    return _optimize_assert(rebuild_ctx, *args, **kwargs)
