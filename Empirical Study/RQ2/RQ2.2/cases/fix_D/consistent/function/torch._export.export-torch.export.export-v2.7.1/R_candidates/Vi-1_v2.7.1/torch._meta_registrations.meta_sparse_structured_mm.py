@register_meta(aten._sparse_semi_structured_mm)
def meta_sparse_structured_mm(
    mat1: Tensor,
    mat1_meta: Tensor,
    mat2: Tensor,
    out_dtype: Optional[torch.dtype] = None,
):
    assert len(mat1.shape) == 2
    assert len(mat1_meta.shape) == 2
    assert len(mat2.shape) == 2
    assert mat1.size(1) == mat2.size(0) / 2
    output_sizes = [mat1.size(0), mat2.size(1)]

    if out_dtype is not None:
        assert mat2.dtype == torch.int8 and out_dtype == torch.int32, (
            "out_dtype is only supported for i8i8->i32 linear operator"
        )
    output = mat2.new_empty(
        output_sizes,
        dtype=mat2.dtype if out_dtype is None else out_dtype,
    )

    return output
