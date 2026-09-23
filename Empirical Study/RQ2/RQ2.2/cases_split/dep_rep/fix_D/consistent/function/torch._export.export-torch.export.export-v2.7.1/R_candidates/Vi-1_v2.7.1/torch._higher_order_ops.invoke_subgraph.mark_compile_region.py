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
            return invoke_subgraph_placeholder(func, *args, **kwargs)

        return inner

    if fn:
        return wrap(fn)
    else:
        return wrap
