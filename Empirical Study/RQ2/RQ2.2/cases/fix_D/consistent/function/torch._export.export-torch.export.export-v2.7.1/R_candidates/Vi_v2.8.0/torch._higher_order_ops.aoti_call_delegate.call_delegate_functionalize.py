@aoti_call_delegate.py_functionalize_impl
def call_delegate_functionalize(
    ctx,
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
):
    unwrapped_weight_args = tuple(
        ctx.unwrap_tensors(weight_arg) for weight_arg in weight_args
    )
    unwrapped_input_args = tuple(
        ctx.unwrap_tensors(input_arg) for input_arg in input_args
    )
    with ctx.redispatch_to_next():
        res = aoti_call_delegate(
            lowered_module, original_gm, unwrapped_weight_args, unwrapped_input_args  # type: ignore[arg-type]
        )
        return ctx.wrap_tensors(res)
