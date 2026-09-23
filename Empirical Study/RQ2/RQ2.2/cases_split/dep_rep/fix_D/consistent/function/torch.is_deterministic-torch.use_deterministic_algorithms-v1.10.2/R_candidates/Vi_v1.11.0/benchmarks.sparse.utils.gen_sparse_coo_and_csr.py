def gen_sparse_coo_and_csr(shape, nnz):
    total_values = functools.reduce(operator.mul, shape, 1)
    dense = np.random.randn(total_values)
    fills = random.sample(list(range(total_values)), total_values - nnz)

    for f in fills:
        dense[f] = 0

    dense = torch.from_numpy(dense.reshape(shape))
    return dense.to_sparse(), dense.to_sparse_csr()
