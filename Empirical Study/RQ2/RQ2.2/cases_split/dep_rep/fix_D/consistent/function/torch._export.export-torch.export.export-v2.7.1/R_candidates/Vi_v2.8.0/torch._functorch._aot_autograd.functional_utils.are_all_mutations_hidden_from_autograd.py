def are_all_mutations_hidden_from_autograd(t):
    if is_traceable_wrapper_subclass(t):
        attrs, _ = t.__tensor_flatten__()
        # If all inner elements are mutations hidden from autograd, then it is a mutation hidden from autograd.
        return all(
            are_all_mutations_hidden_from_autograd(getattr(t, attr)) for attr in attrs
        )
    elif isinstance(t, torch.Tensor):
        assert isinstance(t, FunctionalTensor)
        return torch._functionalize_are_all_mutations_hidden_from_autograd(t.elem)
    else:
        return False
