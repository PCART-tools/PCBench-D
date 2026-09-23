def _adjusted_atol(atol, u, v):
    # In slow gradcheck, we compare A and B element-wise, i.e., for some a, b we
    # allow: |a - b| < atol + rtol * b. But since we now compare q1 = v^T A u and
    # q2 = v^T B u, we must allow |q1 - q2| < v^T E u + rtol * v^T B u, where E is
    # the correctly sized matrix in which each entry is atol.
    #
    # We see that atol needs to be scaled by v^T M u (where M is an all-ones M x N
    # matrix): v^T M u = \sum_{i} \sum_{j} u_i * v_j = (\sum_{i} u_i)(\sum_{i} v_i)
    # TODO: properly handle case when u is tuple instead of only taking first element
    u = u[0] if isinstance(u, tuple) else u
    sum_u = torch.sparse.sum(u) if u.layout == torch.sparse_coo else u.sum()
    sum_v = 1. if v is None else torch.sparse.sum(v) if v.layout == torch.sparse_coo else v.sum()
    return atol * float(sum_u) * float(sum_v)
