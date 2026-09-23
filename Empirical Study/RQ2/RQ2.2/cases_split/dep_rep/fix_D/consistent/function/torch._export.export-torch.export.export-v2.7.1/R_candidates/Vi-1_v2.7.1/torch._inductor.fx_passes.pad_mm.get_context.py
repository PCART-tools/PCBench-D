def get_context(
    mat1: Tensor,
    mat2: Tensor,
    mat1_pre_padded: bool,
    mat2_pre_padded: bool,
    m_padded_length: int,
    k_padded_length: int,
    n_padded_length: int,
) -> AHContext:
    context = AHContext()

    context.add_feature("m", mat1.shape[0])
    context.add_feature("k", mat1.shape[1])
    context.add_feature("n", mat2.shape[1])

    context_add_strides(context, "mat1", mat1.stride())
    context_add_strides(context, "mat2", mat2.stride())

    context.add_feature("m_padded_length", m_padded_length)
    context.add_feature("k_padded_length", k_padded_length)
    context.add_feature("n_padded_length", n_padded_length)

    context.add_feature("mat1_align_size", get_alignment_size(mat1))
    context.add_feature("mat2_align_size", get_alignment_size(mat2))

    context.add_feature("mat1_dtype", mat1.dtype, is_categorical=True)
    context.add_feature("mat2_dtype", mat2.dtype, is_categorical=True)

    context.add_feature("prepadded_mat1", mat1_pre_padded, is_categorical=True)
    context.add_feature("prepadded_mat2", mat2_pre_padded, is_categorical=True)

    context_add_using_tf32(context, mat1.dtype)
    return context
