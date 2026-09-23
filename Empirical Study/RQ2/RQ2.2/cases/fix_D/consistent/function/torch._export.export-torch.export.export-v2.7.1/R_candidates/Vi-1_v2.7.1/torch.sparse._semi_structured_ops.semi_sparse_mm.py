def semi_sparse_mm(func, types, args=(), kwargs=None) -> torch.Tensor:
    assert len(args) == 2
    A, B = args
    if A.ndim != 2 or B.ndim != 2:
        raise NotImplementedError(
            "`SparseSemiStructuredTensor` matmul: Broadcasting is not implemented"
        )
    if isinstance(A, torch.sparse.SparseSemiStructuredTensor):
        row, col = B.shape
        B_padded = A._pad_dense_input(B)
        res = A._mm(B_padded)
        return res[:, :col]
    else:
        B_t = B.t()
        assert isinstance(B_t, torch.sparse.SparseSemiStructuredTensor)
        row, col = A.shape
        A_padded = B._pad_dense_input(A)
        res = B_t._mm(A_padded.t()).t()
        return res[:row, :]
