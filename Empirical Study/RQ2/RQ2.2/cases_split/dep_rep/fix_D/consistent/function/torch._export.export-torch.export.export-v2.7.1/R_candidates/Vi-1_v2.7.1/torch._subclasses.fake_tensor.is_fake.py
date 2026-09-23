def is_fake(x: object) -> TypeGuard[Tensor]:
    from torch._subclasses.functional_tensor import FunctionalTensor

    if isinstance(x, FakeTensor):
        return True
    if is_traceable_wrapper_subclass(x):
        attrs, _ = type(x).__tensor_flatten__(x)
        flattened_tensors = [getattr(x, attr) for attr in attrs]
        all_fake = all(is_fake(x) for x in flattened_tensors)
        any_fake = any(is_fake(x) for x in flattened_tensors)
        assert all_fake == any_fake, "got mixed fake and real tensors!"
        return all_fake
    elif isinstance(x, FunctionalTensor):
        return is_fake(x.elem)
    elif isinstance(x, Tensor) and torch._is_functional_tensor(x):
        reapply_views = torch._C._functionalization_reapply_views_tls()
        unwrapped = torch._C._functorch._unwrap_functional_tensor(x, reapply_views)
        return is_fake(unwrapped)
    elif isinstance(x, Tensor) and is_functorch_wrapped_tensor(x):
        unwrapped = torch._C._functorch.get_unwrapped(x)
        return is_fake(unwrapped)
    return False
