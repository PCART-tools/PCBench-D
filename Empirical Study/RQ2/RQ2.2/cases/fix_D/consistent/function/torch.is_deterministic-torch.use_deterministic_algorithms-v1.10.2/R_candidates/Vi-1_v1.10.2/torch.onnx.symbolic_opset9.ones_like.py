@parse_args("v", "i", "v", "v", "v", "v")
def ones_like(g, input, dtype=None, layout=None, device=None, pin_memory=False, memory_format=None):
    shape = g.op("Shape", input)
    if dtype is None:
        dtype = 6  # float
    return g.op("ConstantOfShape", shape,
                value_t=torch.tensor([1], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
