def _to_flat_dense_if_sparse(tensor):
    if tensor.layout == torch.sparse_coo:
        return tensor.to_dense().reshape(-1)
    else:
        return tensor
