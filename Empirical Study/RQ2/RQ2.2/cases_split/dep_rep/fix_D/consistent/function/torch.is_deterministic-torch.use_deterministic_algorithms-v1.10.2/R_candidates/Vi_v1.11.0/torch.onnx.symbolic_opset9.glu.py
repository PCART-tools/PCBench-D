@parse_args("v", "i")
def glu(g, input, dim):
    dim_size = sym_help._get_tensor_dim_size(input, dim)
    if dim_size is not None:
        assert dim_size % 2 == 0

    first, second = g.op("Split", input, axis_i=dim, outputs=2)
    return g.op("Mul", first, g.op("Sigmoid", second))
