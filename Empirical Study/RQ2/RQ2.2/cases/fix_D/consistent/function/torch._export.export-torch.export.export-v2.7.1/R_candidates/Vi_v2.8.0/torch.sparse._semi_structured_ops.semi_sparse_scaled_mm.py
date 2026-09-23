def semi_sparse_scaled_mm(func, types, args=(), kwargs=None) -> torch.Tensor:
    # pull all args, excluding use_fast_accum flag if set.
    A, B, A_scale, B_scale, bias, scale_result, out_dtype = args[:7]

    assert A.dtype == torch.float8_e4m3fn
    assert B.dtype == torch.float8_e4m3fn
    # only cuSPARSELt supports float8_e4m3fn currently
    assert isinstance(A, torch.sparse.SparseSemiStructuredTensorCUSPARSELT)
    assert A.packed is not None
    # Currently we only support per-tensor scaling, with float32 scales
    assert A_scale.numel() == 1 and B_scale.numel() == 1
    assert A_scale.dtype == torch.float32 and B_scale.dtype == torch.float32

    # cuSPARSELt lacks the A and B operand scaling support, so instead we use alpha to scale the result.
    # Note that this limits us to per-tensor scalig only.
    sparse_result = torch._cslt_sparse_mm(
        A.packed,
        B,
        alpha=A_scale * B_scale,
        out_dtype=out_dtype,
    )
    return sparse_result
