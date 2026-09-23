def register_fake(hop, fn=None):
    """
    Register a fake function for a HOP. This is conceptually equivalent of the
    register_fake utility for the custom ops. The registered function is called
    inside the fake_tensor _dispatch_impl.
    """
    assert hop not in registered_hop_fake_fns

    def register(func: F) -> F:
        from torch._subclasses.fake_tensor import FakeTensorMode

        redirect_to_mode(hop, FakeTensorMode)

        registered_hop_fake_fns[hop] = func
        return func

    if fn is None:
        return register
    return register(fn)
