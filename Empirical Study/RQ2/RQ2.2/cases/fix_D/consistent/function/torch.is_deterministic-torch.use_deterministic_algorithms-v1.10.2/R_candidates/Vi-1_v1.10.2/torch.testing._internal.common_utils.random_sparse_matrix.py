def random_sparse_matrix(rows, columns, density=0.01, **kwargs):
    """Return rectangular random sparse matrix within given density.

    The density of the result approaches to given density as the size
    of the matrix is increased and a relatively small value of density
    is specified but higher than min(rows, columns)/(rows * columns)
    for non-singular matrices.
    """
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')
    singular = kwargs.get("singular", False)

    k = min(rows, columns)
    nonzero_elements = max(min(rows, columns), int(rows * columns * density))

    row_indices = [i % rows for i in range(nonzero_elements)]
    column_indices = [i % columns for i in range(nonzero_elements)]
    random.shuffle(column_indices)
    indices = [row_indices, column_indices]
    values = torch.randn(nonzero_elements, dtype=dtype, device=device)
    # ensure that the diagonal dominates
    values *= torch.tensor([-float(i - j)**2 for i, j in zip(*indices)], dtype=dtype, device=device).exp()
    indices_tensor = torch.tensor(indices)
    A = torch.sparse_coo_tensor(indices_tensor, values, (rows, columns), device=device)
    return A.coalesce()
