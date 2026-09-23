@register_meta(aten._cslt_sparse_mm)
def meta__cslt_sparse_mm(
    compressed_A: torch.Tensor,
    dense_B: torch.Tensor,
    bias: Optional[Tensor] = None,
    alpha: Optional[Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
    transpose_result: bool = False,
    alg_id: int = 0,
    split_k: int = 1,
    split_k_mode: int = -1,
):
    assert dense_B.dtype in {
        torch.float32,
        torch.float16,
        torch.bfloat16,
        torch.int8,
        torch.float8_e4m3fn,
    }, "_cslt_sparse_mm only supports fp16, bf16, int8, and fp8e4m3"
    assert compressed_A.dtype == dense_B.dtype, "inputs must have the same dtype"
    assert len(dense_B.shape) == 2, "_cslt_sparse_mm only supports 2d inputs"

    is_8bit_input_type = compressed_A.dtype in [torch.int8, torch.float8_e4m3fn]
    compression_factor = 10 if is_8bit_input_type else 9

    if is_8bit_input_type:
        assert not dense_B.is_contiguous(), (
            "dense input must be transposed for 8bit dtypes"
        )

    k = dense_B.size(0)
    n = dense_B.size(1)
    m = (compressed_A.numel() * 16) // (compression_factor * k)
    if bias is not None:
        assert m == bias.size(0)

    if out_dtype is not None:
        assert is_8bit_input_type and out_dtype in {
            torch.float16,
            torch.bfloat16,
            torch.int32,
            torch.float8_e4m3fn,
        }, (
            "out_dtype is not supported for {compressed_A.dtype} x {dense_B.dtype} -> {out_dtype} matmul!"
        )
    output_shape = (n, m) if transpose_result else (m, n)
    return dense_B.new_empty(output_shape, dtype=out_dtype)
