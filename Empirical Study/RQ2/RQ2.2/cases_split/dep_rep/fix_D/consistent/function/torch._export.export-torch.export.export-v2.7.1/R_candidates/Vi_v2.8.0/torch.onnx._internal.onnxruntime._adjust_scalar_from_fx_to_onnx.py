def _adjust_scalar_from_fx_to_onnx(
    dynamo_value: Union[
        torch.Tensor,
        int,
        float,
        bool,
    ],
    value_info: "onnx.ValueInfoProto",  # type: ignore[name-defined]
) -> torch.Tensor:
    """Helper function to wrap PyTorch variables as torch.Tensor"""
    if (
        isinstance(dynamo_value, torch.Tensor)
        and len(value_info.type.tensor_type.shape.dim) == 0
        and dynamo_value.shape == (1,)
    ):
        # ONNX expect a scalar with empty shape.
        # In contrast, PyTorch usually allows implicit
        # conversion between shape=() and shape=(1,).
        #
        # Below, PyTorch's shape (1,) is reshaped to ().
        return torch.squeeze(dynamo_value)
    elif isinstance(dynamo_value, int):
        return torch.tensor(dynamo_value, dtype=torch.int64)
    elif isinstance(dynamo_value, float):
        return torch.tensor(dynamo_value, dtype=torch.float32)
    elif isinstance(dynamo_value, bool):
        return torch.tensor(dynamo_value, dtype=torch.bool)
    else:
        assert isinstance(dynamo_value, torch.Tensor)
        return dynamo_value.contiguous()
