def gen_sparse_csr(shape, nnz):
    fill_value = 0
    total_values = functools.reduce(operator.mul, shape, 1)
    dense = np.random.randn(total_values)
    fills = random.sample(list(range(total_values)), total_values - nnz)

    for f in fills:
        dense[f] = fill_value
    dense = torch.from_numpy(dense.reshape(shape))

    return dense.to_sparse_csr()
