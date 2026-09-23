def sparse_grad_output(a, b):
    c = torch.sparse.mm(a, b)
    if c.is_sparse:
        c2 = torch.rand_like(c.to_dense())
        return c2.sparse_mask(c.coalesce())
    else:
        return torch.rand_like(c)
