def basis(A):
    """Return orthogonal basis of A columns.
    """
    if A.is_cuda:
        # torch.orgqr is not available in CUDA
        Q = torch.linalg.qr(A).Q
    else:
        Q = torch.orgqr(*torch.geqrf(A))
    return Q
