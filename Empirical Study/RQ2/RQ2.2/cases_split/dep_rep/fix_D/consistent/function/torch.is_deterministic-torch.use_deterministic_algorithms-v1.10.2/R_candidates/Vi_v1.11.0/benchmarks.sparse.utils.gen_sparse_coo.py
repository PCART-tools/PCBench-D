def gen_sparse_coo(shape, nnz):
    dense = np.random.randn(*shape)
    values = []
    indices = [[], []]
    for n in range(nnz):
        row = random.randint(0, shape[0] - 1)
        col = random.randint(0, shape[1] - 1)
        indices[0].append(row)
        indices[1].append(col)
        values.append(dense[row, col])

    return torch.sparse_coo_tensor(indices, values, size=shape)
