def was_inductor_storage_resized(t):
    if is_traceable_wrapper_subclass(t):
        attrs, _ = t.__tensor_flatten__()
        if any(was_inductor_storage_resized(getattr(t, attr)) for attr in attrs):
            raise RuntimeError(
                f"storage resizing is not supported on tensor subclass: {type(t)}"
            )
    elif not isinstance(t, torch.Tensor):
        return False
    else:
        assert isinstance(t, FunctionalTensor)
        return torch._functionalize_was_inductor_storage_resized(t.elem)
