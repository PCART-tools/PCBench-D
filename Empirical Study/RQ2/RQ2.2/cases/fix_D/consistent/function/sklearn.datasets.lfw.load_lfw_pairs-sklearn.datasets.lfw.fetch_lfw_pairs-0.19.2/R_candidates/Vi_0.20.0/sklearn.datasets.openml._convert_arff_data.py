def _convert_arff_data(arff_data, col_slice_x, col_slice_y):
    """
    converts the arff object into the appropriate matrix type (np.array or
    scipy.sparse.csr_matrix) based on the 'data part' (i.e., in the
    liac-arff dict, the object from the 'data' key)

    Parameters
    ----------
    arff_data : list or dict
        as obtained from liac-arff object

    col_slice_x : list
        The column indices that are sliced from the original array to return
        as X data

    col_slice_y : list
        The column indices that are sliced from the original array to return
        as y data

    Returns
    -------
    X : np.array or scipy.sparse.csr_matrix
    y : np.array
    """
    if isinstance(arff_data, list):
        data = np.array(arff_data, dtype=np.float64)
        X = np.array(data[:, col_slice_x], dtype=np.float64)
        y = np.array(data[:, col_slice_y], dtype=np.float64)
        return X, y
    elif isinstance(arff_data, tuple):
        arff_data_X = _split_sparse_columns(arff_data, col_slice_x)
        num_obs = max(arff_data[1]) + 1
        X_shape = (num_obs, len(col_slice_x))
        X = scipy.sparse.coo_matrix(
            (arff_data_X[0], (arff_data_X[1], arff_data_X[2])),
            shape=X_shape, dtype=np.float64)
        X = X.tocsr()
        y = _sparse_data_to_array(arff_data, col_slice_y)
        return X, y
    else:
        # This should never happen
        raise ValueError('Unexpected Data Type obtained from arff.')
