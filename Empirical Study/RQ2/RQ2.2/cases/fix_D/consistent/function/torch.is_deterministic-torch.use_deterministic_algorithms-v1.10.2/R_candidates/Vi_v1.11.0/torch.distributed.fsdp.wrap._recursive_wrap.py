def _recursive_wrap(
    module: nn.Module,
    auto_wrap_policy: Callable,
    wrapper_cls: Callable,
    only_wrap_children: bool = False,
    **kwargs: Any
) -> Tuple[nn.Module, int]:
    """
    Automatically wrap child modules of *module* that meet the given
    criteria with :func:`auto_wrap`. Does not rely on ConfigAutoWrap.
    Args:
        module (nn.Module):
            module to recursively wrap
        auto_wrap_policy (Callable):
            A callable specifying a policy to recursively wrap layers with FSDP.
    Returns:
        (nn.Module, int):
            Wrapped module and the number parameters wrapped recursively.
    """
    assert auto_wrap_policy is not None, "Must specify auto_wrap_policy."
    assert wrapper_cls is not None, "Must specify wrapper_cls"
    # Make sure no child is already wrapped.
    for _, child in module.named_modules():
        assert not isinstance(child, cast(type, wrapper_cls))

    # We count all params, assuming none of them is already wrapped.
    num_params = sum([p.numel() for p in module.parameters()])

    assert auto_wrap_policy is not None
    if auto_wrap_policy(module=module, recurse=True, unwrapped_params=num_params):
        total_wrapped_params = 0
        # Iterate through the children, recursively wrap if necessary
        for name, child in module.named_children():
            wrapped_child, num_wrapped_params = _recursive_wrap(
                module=child,
                auto_wrap_policy=auto_wrap_policy,
                wrapper_cls=wrapper_cls,
                **kwargs,
            )
            setattr(module, name, wrapped_child)
            # Keep track of how many parameters have been wrapped
            total_wrapped_params += num_wrapped_params
        # decide if we need to wrap the current module,
        # since the left over parameters exceed the number of params to wrap
        remainder = num_params - total_wrapped_params
        if not only_wrap_children and auto_wrap_policy(
            module=module, recurse=False, unwrapped_params=remainder
        ):
            # Leaf node or final wrapping of the remainder both happen here.
            return _wrap(module, wrapper_cls, **kwargs), num_params
        else:
            return module, total_wrapped_params
    return module, 0
