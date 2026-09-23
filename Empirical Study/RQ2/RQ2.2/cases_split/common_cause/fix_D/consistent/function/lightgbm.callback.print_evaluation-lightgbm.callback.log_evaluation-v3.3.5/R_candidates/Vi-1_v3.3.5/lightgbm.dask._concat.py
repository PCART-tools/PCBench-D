def _concat(seq: List[_DaskPart]) -> _DaskPart:
    if isinstance(seq[0], np.ndarray):
        return np.concatenate(seq, axis=0)
    elif isinstance(seq[0], (pd_DataFrame, pd_Series)):
        return concat(seq, axis=0)
    elif isinstance(seq[0], ss.spmatrix):
        return ss.vstack(seq, format='csr')
    else:
        raise TypeError(f'Data must be one of: numpy arrays, pandas dataframes, sparse matrices (from scipy). Got {type(seq[0]).__name__}.')
