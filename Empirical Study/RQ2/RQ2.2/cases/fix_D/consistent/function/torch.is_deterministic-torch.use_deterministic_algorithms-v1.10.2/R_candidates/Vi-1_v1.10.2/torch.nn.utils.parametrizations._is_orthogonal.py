def _is_orthogonal(Q, eps=None):
    n, k = Q.size(-2), Q.size(-1)
    Id = torch.eye(k, dtype=Q.dtype, device=Q.device)
    # A reasonable eps, but not too large
    eps = 10. * n * torch.finfo(Q.dtype).eps
    return torch.allclose(Q.transpose(-2, -1).conj() @ Q, Id, atol=eps)
