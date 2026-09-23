@parse_args("v", "i", "v", "v", "v")
def zeros(g, sizes, dtype, layout, device, pin_memory=False):
    # NOTE: no way to set device, layout and pin_memory in ONNX, so we ignore it
    if dtype is None:
        dtype = ScalarType.FLOAT
    sizes_ = sym_help._maybe_get_const(sizes, "is")
    if isinstance(sizes_, list) and len(sizes_) == 0:
        sizes = g.op("Constant", value_t=torch.tensor([]).to(torch.int64))
    return g.op("ConstantOfShape", sizes,
                value_t=torch.tensor([0], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
