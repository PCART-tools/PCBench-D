def are_all_mutations_under_no_grad_or_inference_mode(t):
    if is_traceable_wrapper_subclass(t):
        attrs, _ = t.__tensor_flatten__()
        return all(
            are_all_mutations_under_no_grad_or_inference_mode(getattr(t, attr))
            for attr in attrs
        )
    else:
        assert isinstance(t, FunctionalTensor)
        return torch._functionalize_are_all_mutations_under_no_grad_or_inference_mode(
            t.elem
        )
