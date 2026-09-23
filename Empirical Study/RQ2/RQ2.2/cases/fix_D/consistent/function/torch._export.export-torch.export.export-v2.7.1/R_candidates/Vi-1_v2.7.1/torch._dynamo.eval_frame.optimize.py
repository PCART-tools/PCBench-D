def optimize(*args, **kwargs):
    def rebuild_ctx():
        ca_kwargs_override = config.compiled_autograd_kwargs_override
        if ca_kwargs_override:
            # NOTE: The process of translating other `torch.compile` kwargs to `torch._dynamo.optimize` kwargs
            # is more complicated, we will add it in the future when needed.
            assert set(ca_kwargs_override.keys()) == {"fullgraph"}, (
                f"Only `fullgraph` kwarg override is supported for now, but got {ca_kwargs_override.keys()}"
            )
            kwargs["nopython"] = ca_kwargs_override["fullgraph"]
        return optimize(*args, **kwargs)

    return _optimize(rebuild_ctx, *args, **kwargs)
