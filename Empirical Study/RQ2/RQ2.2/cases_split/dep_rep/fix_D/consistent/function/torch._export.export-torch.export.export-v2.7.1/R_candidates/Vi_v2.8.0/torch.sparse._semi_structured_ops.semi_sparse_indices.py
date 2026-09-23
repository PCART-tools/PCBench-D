def semi_sparse_indices(func, types, args=(), kwargs=None) -> torch.Tensor:
    assert len(args) == 1
    A = args[0]
    assert isinstance(A, torch.sparse.SparseSemiStructuredTensor)
    assert A.packed is not None
    if A.meta is None:
        m, k = A.shape
        num_kept_elements = m * k // 2
        metadata = A.packed[num_kept_elements:].view(m, -1)
        return metadata.view(torch.int32 if A.dtype == torch.int32 else torch.int16)
    else:
        return A.meta
