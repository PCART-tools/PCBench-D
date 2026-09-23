@aoti_call_delegate.py_impl(torch._C.DispatchKey.CompositeExplicitAutograd)
# pyre-ignore
def call_delegate_cpu(
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
) -> list[torch.Tensor]:
    # FX creates this immutable_dict/list concept. Get rid of this.
    map_types: dict[type, type] = {
        torch.fx.immutable_collections.immutable_dict: dict,
        torch.fx.immutable_collections.immutable_list: list,
    }
    new_args = pytree.tree_map_only(
        tuple(map_types.keys()),
        lambda a: map_types[type(a)](a),
        input_args,
        lambda a: isinstance(a, tuple(map_types.keys())),
    )

    has_fake_input_args = any(isinstance(arg, FakeTensor) for arg in new_args)
    has_fake_params = any(
        isinstance(param, FakeTensor) for param in original_gm.parameters()
    )
    has_fake_buffers = any(
        isinstance(buffer, FakeTensor) for buffer in original_gm.buffers()
    )

    if has_fake_input_args or has_fake_params or has_fake_buffers:
        # aoti lowered module doesn't support fake tensor
        return original_gm(*new_args)
    else:
        return lowered_module(new_args)  # type: ignore[misc]
