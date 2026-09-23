@register_decomposition(aten.upsample_bicubic2d.vec)
@aten.upsample_bicubic2d.vec.py_impl(DispatchKey.CompositeImplicitAutograd)
@aten.upsample_bicubic2d.vec.py_impl(DispatchKey.Autograd)
@out_wrapper()
@pw_cast_for_opmath
def upsample_bicubic2d_vec(
    a: Tensor,
    output_size: Optional[tuple[int, int]],
    align_corners: bool,
    scale_factors: Optional[tuple[float, float]] = None,
) -> Tensor:
    torch._check(
        bool(output_size) + bool(scale_factors) == 1,
        lambda: "Must specify exactly one of output_size and scale_factors.",
    )
    if output_size is None:
        assert scale_factors is not None
        output_size = cast(
            tuple[int, int],
            tuple(
                sym_int(sym_float(w) * scale)
                for w, scale in zip(a.shape[2:], scale_factors)
            ),
        )
    scale_h, scale_w = scale_factors if scale_factors else (None, None)
    return upsample_bicubic2d_default(a, output_size, align_corners, scale_h, scale_w)
