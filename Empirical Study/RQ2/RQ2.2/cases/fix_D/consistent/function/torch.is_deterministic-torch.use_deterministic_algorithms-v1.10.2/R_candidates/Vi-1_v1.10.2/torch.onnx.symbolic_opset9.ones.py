@parse_args("v", "i", "v", "v", "v")
def ones(g, sizes, dtype, layout, device, pin_memory=False):
    if dtype is None:
        dtype = 6  # float
    return g.op("ConstantOfShape", sizes,
                value_t=torch.tensor([1], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
