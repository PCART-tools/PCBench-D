@register_op_impl(torch.ops.aten._assert_tensor_metadata.default)
def assert_tensor_metadata(
    fake_mode,
    func,
    t,
    sizes=None,
    strides=None,
    dtype=None,
    *,
    device=None,
    layout=None,
) -> None:
    if sizes is not None:
        assert (
            t.size() == sizes
        ), f"Tensor sizes mismatch! Expected: {sizes}, Got: {t.size()}"
    if strides is not None:
        assert (
            t.stride() == strides
        ), f"Tensor strides mismatch! Expected: {strides}, Got: {t.stride()}"
    if dtype is not None:
        assert (
            t.dtype == dtype
        ), f"Tensor dtype mismatch! Expected: {dtype}, Got: {t.dtype}"
    if layout is not None:
        assert (
            t.layout == layout
        ), f"Tensor layout mismatch! Expected: {layout}, Got: {t.layout()}"
    if device is not None:
        assert (
            t.device == device
        ), f"Tensor device mismatch! Expected: {device}, Got: {t.device}"
