@aoti_call_delegate.py_impl(FakeTensorMode)
def call_delegate_fake_tensor_mode(
    mode: FakeTensorMode,
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
) -> list[torch.Tensor]:
    with mode:
        return call_delegate_cpu(lowered_module, original_gm, weight_args, input_args)
