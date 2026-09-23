def maybe_to_fake_obj(
    fake_mode, x: torch.ScriptObject
) -> Union[FakeScriptObject, torch.ScriptObject]:
    import torch.utils._pytree as pytree
    from torch.utils._python_dispatch import _disable_current_modes

    # When tracing with real mode, people should implement meta kernels that can
    # handle the case of real script object + fake tensor inputs.
    if tracing_with_real(x):
        return x

    # x.__obj_flatten__() could be calling some tensor operations inside but we don't
    # want to call these ops in surrounding dispatch modes when executing it.
    # Otherwise, for example, the fake tensor modes will error out when the tensors inside
    # script obeject execute some operations like clone if allow_non_fake_input flag is set.
    with _disable_current_modes():
        flat_x = x.__obj_flatten__()  # type: ignore[attr-defined]

    _check_valid_flat_script_obj(flat_x)

    fake_flattened = pytree.tree_map_only(
        torch.Tensor,
        lambda t: fake_mode.from_tensor(t),
        flat_x,
    )

    fake_x = _find_fake_class_for_script_object(x).__obj_unflatten__(fake_flattened)

    fake_x_wrapped = FakeScriptObject(fake_x, x._type().qualified_name(), x)  # type: ignore[attr-defined]

    for name in x._method_names():  # type: ignore[attr-defined]
        attr = getattr(fake_x, name, None)
        if attr:
            if not callable(attr):
                raise RuntimeError(f"Expect {name} to be a callable but got {attr}.")

            real_attr = getattr(x, name)  # type: ignore[attr-defined]

            # real attr sometimes is not torch.ScriptMethod thus doesn't have schema e.g. __init___ or __eq__
            method_schema: Optional[torch.FunctionSchema] = None
            if isinstance(real_attr, torch.ScriptMethod):
                method_schema = real_attr.schema  # type: ignore[attr-defined]

            setattr(
                fake_x_wrapped,
                name,
                FakeScriptMethod(fake_x_wrapped, name, method_schema),
            )
        else:
            override_skip_list = {"__obj_flatten__", "__get_state__", "__set_state__"}
            if name not in override_skip_list:
                log.warning("fake object of %s doesn't implement method %s.", x, name)
    return fake_x_wrapped
