def mark_compile_region(fn=None):
    """
    This wrapper instructs torch.compile to compile the wrapped region once and
    reuse the compiled artifact, instead of the usual way of aggressively
    inlining the function.

    Under the hood, it tells TorchDynamo to use InvokeSubgraph HOP for the
    region. For PyTorch eager, this is a no-op.
    """

    def wrap(func):
        def inner(*args, **kwargs):
            # Get the innermost function to avoid nested compile regions
            inner_func = func
            while hasattr(inner_func, "__marked_compile_region_fn__"):
                inner_func = inner_func.__marked_compile_region_fn__
            return invoke_subgraph_placeholder(inner_func, *args, **kwargs)

        inner.__marked_compile_region_fn__ = func  # type: ignore[attr-defined]

        return inner

    if fn:
        return wrap(fn)
    else:
        return wrap
