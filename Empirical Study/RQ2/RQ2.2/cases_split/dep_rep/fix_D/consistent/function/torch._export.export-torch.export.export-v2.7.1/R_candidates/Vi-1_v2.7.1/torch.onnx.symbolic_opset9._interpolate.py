@_onnx_symbolic(
    "aten::upsample_nearest1d",
    decorate=[
        symbolic_helper._apply_params("upsample_nearest1d", 3, "nearest"),
        _export("upsample_nearest1d"),
    ],
)
@_onnx_symbolic(
    "aten::upsample_nearest2d",
    decorate=[
        symbolic_helper._apply_params("upsample_nearest2d", 4, "nearest"),
        _export("upsample_nearest2d"),
    ],
)
@_onnx_symbolic(
    "aten::upsample_nearest3d",
    decorate=[
        symbolic_helper._apply_params("upsample_nearest3d", 5, "nearest"),
        _export("upsample_nearest3d"),
    ],
)
@_onnx_symbolic(
    "aten::upsample_linear1d",
    decorate=[
        symbolic_helper._apply_params("upsample_linear1d", 3, "linear"),
        _export("upsample_linear1d"),
    ],
)
@_onnx_symbolic(
    "aten::upsample_bilinear2d",
    decorate=[
        symbolic_helper._apply_params("upsample_bilinear2d", 4, "linear"),
        _export("upsample_bilinear2d"),
    ],
)
@_onnx_symbolic(
    "aten::upsample_trilinear3d",
    decorate=[
        symbolic_helper._apply_params("upsample_trilinear3d", 5, "linear"),
        _export("upsample_trilinear3d"),
    ],
)
def _interpolate(name: str, dim: int, interpolate_mode: str):
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = symbolic_helper._get_interpolate_attributes(
            g, interpolate_mode, args
        )
        symbolic_helper._interpolate_warning(interpolate_mode)
        align_corners = symbolic_helper._maybe_get_scalar(align_corners)
        if align_corners:
            return symbolic_helper._unimplemented(name, "align_corners == True", input)
        if scales is None:
            scales = symbolic_helper._interpolate_size_to_scales(
                g, input, output_size, dim
            )
        return g.op("Upsample", input, scales, mode_s=interpolate_mode)

    return symbolic_fn
