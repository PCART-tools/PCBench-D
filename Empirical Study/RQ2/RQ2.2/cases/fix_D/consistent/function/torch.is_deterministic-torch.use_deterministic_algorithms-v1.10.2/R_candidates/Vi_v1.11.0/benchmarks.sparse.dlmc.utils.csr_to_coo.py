def csr_to_coo(indices, indptr, shape):
    n_rows, n_cols = shape
    cols = indices
    rows = [0] * len(cols)
    for i in range(n_rows):
        for j in range(indptr[i], indptr[i + 1]):
            rows[j] = i
    return torch.tensor([rows, cols], dtype=torch.long)
