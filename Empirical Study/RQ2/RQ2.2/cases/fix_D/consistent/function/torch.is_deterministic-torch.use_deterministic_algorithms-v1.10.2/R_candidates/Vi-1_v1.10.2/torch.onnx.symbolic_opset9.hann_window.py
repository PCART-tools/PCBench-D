@parse_args("v", "b", "i", "v", "v", "v", "v")
def hann_window(g, window_length, periodic=True, dtype=None, layout=None, device=None, pin_memory=None, requires_grad=False):
    if dtype is None:
        dtype = torch.get_default_dtype()
        if sym_help._dtype_is_fp(dtype) is False:
            dtype = torch.float
        dtype = sym_help.scalar_type_to_pytorch_type.index(dtype)

    n_array = arange(g, window_length, 4, None, None, None)
    output = g.op("Cast", n_array, to_i=sym_help.cast_pytorch_to_onnx["Float"])
    output = mul(g, g.op("Constant", value_t=torch.tensor(math.pi, dtype=torch.float)), output)

    if periodic is False:
        window_length = sub(g, window_length, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int)))
    output = div(g, output, window_length)
    output = g.op("Cast", square(g, sin(g, output)), to_i=sym_help.scalar_type_to_onnx[dtype])

    return output
