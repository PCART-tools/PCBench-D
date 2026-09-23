def _maybe_wrap_fsdp(model, wrap_fsdp, *args, **kwargs):
    return (
        model if not wrap_fsdp
        else FullyShardedDataParallel(model, *args, **kwargs)
    )
