def semi_sparse_addmm(func, types, args=(), kwargs=None) -> torch.Tensor:
    assert len(args) == 3
    bias, A, B = args
    if A.ndim != 2 or B.ndim != 2:
        raise NotImplementedError(
            "`SparseSemiStructuredTensor` matmul: Broadcasting is not implemented"
        )
    if bias.ndim != 1:
        raise NotImplementedError(
            f"`SparseSemiStructuredTensor` matmul: only bias dim=1 supported. Shape={bias.shape}"
        )
    if isinstance(A, torch.sparse.SparseSemiStructuredTensor):
        raise NotImplementedError(
            "`SparseSemiStructuredTensor` matmul: only operand B of `addmm` can be sparse"
        )
    B_t = B.t()
    assert isinstance(B_t, torch.sparse.SparseSemiStructuredTensor)
    row, _col = A.shape
    A_padded = B_t._pad_dense_input(A)
    result = B_t._mm(A_padded.t(), bias=bias).t()
    return result[:row, :]
