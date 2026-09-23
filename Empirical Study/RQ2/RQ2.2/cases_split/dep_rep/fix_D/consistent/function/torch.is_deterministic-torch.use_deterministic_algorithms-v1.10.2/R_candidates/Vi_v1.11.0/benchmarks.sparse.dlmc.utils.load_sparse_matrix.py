def load_sparse_matrix(path, device):
    with open(path, 'r') as file:
        nrows, ncols, nnz = map(lambda el: int(el), file.readline().split(', '))
        index_pointers = map(lambda el: int(el), file.readline().split())
        indices = map(lambda el: int(el), file.readline().split())

    index_pointers = list(index_pointers)
    indices = list(indices)
    data = torch.randn(nnz, dtype=torch.double)
    shape = (nrows, ncols)
    return torch.sparse_coo_tensor(csr_to_coo(indices, index_pointers, shape), data, shape, device=device)
