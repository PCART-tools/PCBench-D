def _orthogonalize(matrices, epsilon=0):
    """
    Decide between Gram-Schmidt or QR factorization to orthogonalize a batch of matrices.

    QR factorization doesn't work with half-precision, but it is usually faster with a rank > 2.
    """
    assert len(matrices.shape) == 3 and matrices.shape[2] <= matrices.shape[1]

    num_matrices = matrices.shape[0]
    rank = matrices.shape[2]
    dtype = matrices.dtype
    if rank <= 2 or dtype in [torch.float16, torch.bfloat16]:
        _orthogonalize_gram_schmidt(matrices, epsilon=epsilon)
    else:
        torch.linalg.qr(
            matrices,
            out=(
                matrices,
                torch.empty(
                    num_matrices, rank, rank, device=matrices.device, dtype=dtype
                ),
            ),
        )
