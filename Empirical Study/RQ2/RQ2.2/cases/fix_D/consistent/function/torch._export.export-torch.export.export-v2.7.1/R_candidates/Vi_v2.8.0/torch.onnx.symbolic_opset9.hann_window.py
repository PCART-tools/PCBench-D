@_onnx_symbolic("aten::hann_window")
@symbolic_helper.parse_args("v", "b", "i", "v", "v", "v", "v")
def hann_window(
    g: jit_utils.GraphContext,
    window_length,
    periodic=True,
    dtype: int | None = None,
    layout=None,
    device=None,
    pin_memory=None,
    requires_grad=False,
):
    if dtype is None:
        dtype_ = torch.get_default_dtype()
        if not dtype_ or not dtype_.is_floating_point:
            dtype_ = torch.float
        scalar_type = _type_utils.JitScalarType.from_dtype(dtype_)
    else:
        scalar_type = _type_utils.JitScalarType(dtype)

    n_array = arange(g, window_length, 4, None, None, None)
    output = g.op("Cast", n_array, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    output = mul(
        g, g.op("Constant", value_t=torch.tensor(math.pi, dtype=torch.float)), output
    )

    if periodic is False:
        window_length = sub(
            g, window_length, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int))
        )
    output = div(g, output, window_length)
    output = g.op(
        "Cast",
        square(g, sin(g, output)),
        to_i=scalar_type.onnx_type(),
    )

    return output
