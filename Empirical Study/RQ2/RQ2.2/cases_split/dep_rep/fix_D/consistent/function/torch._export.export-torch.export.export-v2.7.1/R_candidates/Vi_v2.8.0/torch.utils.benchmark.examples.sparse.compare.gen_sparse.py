def gen_sparse(size, density, dtype, device='cpu'):
    sparse_dim = len(size)
    nnz = int(size[0] * size[1] * density)
    indices, values = generate_coo_data(size, sparse_dim, nnz, dtype, device)
    return torch.sparse_coo_tensor(indices, values, size, dtype=dtype, device=device)
