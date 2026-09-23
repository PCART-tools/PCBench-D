def gen_vector(path, device):
    with open(path, 'r') as file:
        nrows, ncols, nnz = map(lambda el: int(el), file.readline().split(', '))
        index_pointers = map(lambda el: int(el), file.readline().split())
        indices = map(lambda el: int(el), file.readline().split())
        return torch.randn(nrows, dtype=torch.double, device=device)
