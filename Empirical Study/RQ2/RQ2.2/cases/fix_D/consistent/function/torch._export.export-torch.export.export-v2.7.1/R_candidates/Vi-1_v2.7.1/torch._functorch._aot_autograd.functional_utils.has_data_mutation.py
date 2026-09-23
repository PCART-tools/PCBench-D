def has_data_mutation(t):
    if is_traceable_wrapper_subclass(t):
        attrs, _ = t.__tensor_flatten__()
        # A tensor subclass was updated if any of its inner elements were updated
        return any(has_data_mutation(getattr(t, attr)) for attr in attrs)
    else:
        if isinstance(t, torch.Tensor):
            assert isinstance(t, FunctionalTensor)
            return torch._functionalize_has_data_mutation(t.elem)  # type: ignore[attr-defined]
        return False
