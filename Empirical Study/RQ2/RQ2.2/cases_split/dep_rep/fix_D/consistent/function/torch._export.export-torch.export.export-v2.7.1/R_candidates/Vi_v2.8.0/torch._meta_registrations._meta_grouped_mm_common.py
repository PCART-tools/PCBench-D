def _meta_grouped_mm_common(
    mat_a: Tensor,
    mat_b: Tensor,
    scale_a: Optional[torch.Tensor],
    scale_b: Optional[torch.Tensor],
    offs: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    scale_result: Optional[torch.Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
):
    torch._check(
        (scale_a is None) == (scale_b is None),
        lambda: "Either both scale factors are given, or none",
    )
    scaled = scale_a is not None and scale_b is not None

    # Implementing all the checks from
    # _grouped_mm_cuda()/_scaled_grouped_mm_cuda() code in
    # aten/src/ATen/native/cuda/Blas.cpp.

    if scaled:
        torch._check(
            mat_a.dtype == torch.float8_e4m3fn and mat_b.dtype == torch.float8_e4m3fn,
            lambda: f"Expected inputs of E4M3 FP8 type but got mat_a.dtype={mat_a.dtype} and mat_b.dtype={mat_b.dtype}.",
        )
    else:
        torch._check(
            mat_a.dtype == torch.bfloat16 and mat_b.dtype == torch.bfloat16,
            lambda: f"Expected inputs of BF16 type but got mat_a.dtype={mat_a.dtype} and mat_b.dtype={mat_b.dtype}.",
        )

    torch._check(
        mat_a.dim() in [2, 3] and mat_b.dim() in [2, 3],
        lambda: f"Multiplicands must be 2D or 3D but got mat_a.dim()={mat_a.dim()} and mat_b.dim()={mat_b.dim()}",
    )

    mat_a_is_2d = mat_a.dim() == 2
    mat_b_is_2d = mat_b.dim() == 2

    if scaled:

        def is_row_major(mat):
            mat_stride = mat.stride()
            return mat_stride[-2] > 1 and mat_stride[-1] == 1

        def is_col_major(mat):
            mat_stride = mat.stride()
            return mat_stride[-2] == 1 and mat_stride[-1] > 1

        torch._check(
            is_row_major(mat_a),
            lambda: f"Expected mat_a tensor to be row major in the last two dimensions, got strides {mat_a.stride()[-2:]}",
        )
        torch._check(
            is_col_major(mat_b),
            lambda: f"Expected mat_b tensor to be column major in the last two dimensions, got strides {mat_b.stride()[-2:]}",
        )

    def check_valid_strides(mat_name, mat):
        end_dim = mat.dim() - 1
        alignment = 16 // mat.element_size()
        mat_stride = mat.stride()
        if mat_stride[end_dim - 1] == 1 and mat_stride[end_dim] >= max(
            1, mat.shape[end_dim - 1]
        ):
            torch._check(
                mat_stride[end_dim] % alignment == 0,
                lambda: f"Expected {mat_name} stride along {end_dim} dim to be multiple of 16 bytes, got {mat_stride[end_dim]}.",
            )
        elif mat_stride[end_dim] == 1 and mat_stride[end_dim - 1] >= max(
            1, mat.shape[end_dim]
        ):
            torch._check(
                mat_stride[end_dim - 1] % alignment == 0,
                lambda: f"Expected {mat_name} stride along {end_dim - 1} dim to be multiple of 16 bytes, got {mat_stride[end_dim - 1]}.",  # noqa: B950
            )
        else:
            torch._check(
                False,
                lambda: f"Invalid strides/sizes, got {mat_stride} for strides and {mat.shape} for sizes.",  # noqa: B950
            )

    check_valid_strides("mat_a", mat_a)
    check_valid_strides("mat_b", mat_b)

    if scale_a is not None and scale_b is not None:
        torch._check(
            scale_a.dtype == torch.float32 and scale_b.dtype == torch.float32,
            lambda: "Both scale_a and scale_b must be float (fp32) tensors, but got scale_a.dtype={scale_a.dtype} and scale_b.dtype={scale_b.dtype}.",  # noqa: B950
        )

        def check_scale(scale_name, scale, mat, scaled_dim, scale_multiplier=1):
            if mat.dim() == 2:
                torch._check(
                    scale.dim() == 1,
                    lambda: f"Expected {scale_name} to be 1D tensor, but got {scale.dim()}D tensor.",
                )
                torch._check(
                    scale.is_contiguous(),
                    lambda: f"Expected {scale_name} to be contiguous.",
                )
                torch._check(
                    scale.shape[0] == mat.shape[scaled_dim] * scale_multiplier,
                    lambda: f"Expected {scale_name} to have {mat.shape[scaled_dim] * scale_multiplier} elements, got {scale.shape[0]} elements.",  # noqa: B950
                )
            else:
                torch._check(
                    scale.dim() == 2,
                    lambda: f"Expected {scale_name} to be 2D tensor, but got {scale.dim()}D tensor.",
                )
                torch._check(
                    scale.stride(1) == 1,
                    lambda: f"Expected {scale_name} to be contiguous in the last dimension.",
                )
                torch._check(
                    scale.shape[0] == mat.shape[0],
                    lambda: f"Expected {scale_name} batch dimension to be {mat.shape[0]}, got {scale.shape[0]}.",
                )
                torch._check(
                    scale.shape[1] == mat.shape[1 + scaled_dim],
                    lambda: f"Expected {scale_name} non-batch dimension to be {mat.shape[1 + scaled_dim]}, got {scale.shape[1]}.",
                )

        scale_multiplier = (
            offs.shape[0] if offs is not None and mat_a_is_2d and mat_b_is_2d else 1
        )
        check_scale("scale_a", scale_a, mat_a, 0, scale_multiplier)
        check_scale("scale_b", scale_b, mat_b, 1, scale_multiplier)

        torch._check(
            scale_result is None,
            lambda: "Scale result tensor provided, but it is not supported yet.",
        )

    if mat_a_is_2d or mat_b_is_2d:
        torch._check(
            offs is not None,
            lambda: f"Offsets tensor not provided, but is needed for {mat_a.dim()}D/{mat_b.dim()}D multiplicand layouts.",
        )
        if offs is not None:  # to silence Mypy
            torch._check(
                offs.dim() == 1,
                lambda: f"Offsets tensor must be 1D, but got offs.dim()={offs.dim()}.",
            )
            torch._check(
                offs.dtype == torch.int32,
                lambda: f"Offsets tensor must be integer (int32) tensor, but got {offs.dtype}.",
            )
    else:
        torch._check(
            offs is None,
            lambda: "Offsets tensor provided, but is not needed for 3D/3D multiplicand layouts.",
        )

    torch._check(
        bias is None,
        lambda: "Bias tensor provided, but it is not supported yet.",
    )

    torch._check(
        out_dtype is None or out_dtype == torch.bfloat16,
        lambda: "If output dtype provided, it must be torch.bfloat16.",
    )

    return _create_grouped_mm_output_tensor(mat_a, mat_b, offs, out_dtype)
