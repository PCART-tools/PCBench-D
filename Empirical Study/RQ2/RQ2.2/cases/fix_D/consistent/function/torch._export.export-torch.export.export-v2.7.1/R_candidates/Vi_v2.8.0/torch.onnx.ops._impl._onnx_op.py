def _onnx_op(op_type: str, opset_version: int) -> Callable[[_T], _T]:
    """Decorator to register an ONNX operator with a custom implementation."""

    def decorator(func: _T) -> _T:
        overload = f"opset{opset_version}"
        torch_op = torch.library.custom_op(
            f"onnx::{op_type}.{overload}", mutates_args=()
        )(func)
        ONNX_ATEN_DECOMP_TABLE[getattr(getattr(torch.ops.onnx, op_type), overload)] = (
            func  # type: ignore[assignment]
        )
        # Use the same implementation for the fake implementation
        # This is possible because we use pure aten ops to implement ONNX ops
        torch_op.register_fake(func)
        return torch_op  # type: ignore[return-value]

    return decorator
