def _apply_func_to_inner_tensors_of_same_dim(func, t, *args, **kwargs):
    assert is_traceable_wrapper_subclass(t)

    attrs, _ctx = t.__tensor_flatten__()
    assert isinstance(t, torch.Tensor)
    for attr in attrs:
        inner = getattr(t, attr)
        if inner.dim() == t.dim():
            func(inner, *args, **kwargs)
