def _make_sparse(grad, grad_indices, values):
    size = grad.size()
    return torch.sparse_coo_tensor(grad_indices, values, size)
