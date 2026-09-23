@parse_args("v", "i", "v", "v", "v")
def zeros(g, sizes, dtype, layout, device, pin_memory=False):
    # NOTE: no way to set device, layout and pin_memory in ONNX, so we ignore it
    if dtype is None:
        dtype = 6  # float
    return g.op("ConstantOfShape", sizes,
                value_t=torch.tensor([0], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
