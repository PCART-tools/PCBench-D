def sync_functional_tensor(t):
    if is_traceable_wrapper_subclass(t):
        attrs, _ctx = t.__tensor_flatten__()  # type: ignore[attr-defined]
        for attr in attrs:
            sync_functional_tensor(getattr(t, attr))
    else:
        torch._sync(t)
