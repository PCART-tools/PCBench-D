def use_cpp_bmm_template(
    layout: Layout, mat1: Union[ReinterpretView, Buffer], mat2: IRNode
) -> bool:
    from .ir import Layout

    assert isinstance(mat1.layout, Layout)

    return (
        use_cpp_gemm_template(layout, mat1, mat2, require_constant_mat2=False)
        and mat1.layout.is_contiguous()
    )
