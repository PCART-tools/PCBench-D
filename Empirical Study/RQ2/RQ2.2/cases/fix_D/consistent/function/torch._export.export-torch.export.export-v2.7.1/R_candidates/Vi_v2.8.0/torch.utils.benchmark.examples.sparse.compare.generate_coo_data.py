def generate_coo_data(size, sparse_dim, nnz, dtype, device):
    """
    Parameters
    ----------
    size : tuple
    sparse_dim : int
    nnz : int
    dtype : torch.dtype
    device : str
    Returns
    -------
    indices : torch.tensor
    values : torch.tensor
    """
    if dtype is None:
        dtype = 'float32'

    indices = torch.rand(sparse_dim, nnz, device=device)
    indices.mul_(torch.tensor(size[:sparse_dim]).unsqueeze(1).to(indices))
    indices = indices.to(torch.long)
    values = torch.rand([nnz, ], dtype=dtype, device=device)
    return indices, values
