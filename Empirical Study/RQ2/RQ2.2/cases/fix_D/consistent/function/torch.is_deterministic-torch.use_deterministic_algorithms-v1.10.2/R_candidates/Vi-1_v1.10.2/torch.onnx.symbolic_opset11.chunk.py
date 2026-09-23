def chunk(g, self, chunks, dim):
    # Calculate chunk size for dynamic chunk
    dim_size = g.op("Gather", g.op("Shape", self), dim, axis_i=0)
    chunk_size_s = g.op("Sub", chunks, g.op("Constant", value_t=torch.tensor([1], dtype=torch.long)))
    chunk_size = g.op("Div", g.op("Add", dim_size, chunk_size_s), chunks)
    # Create splits vector
    chunk_vec = [expand(g, chunk_size, chunk_size_s, None),
                 g.op("Sub", dim_size, g.op("Mul", chunk_size, chunk_size_s))]
    chunk_vec = g.op("Concat", *chunk_vec, axis_i=0)
    return split(g, self, chunk_vec, dim)
