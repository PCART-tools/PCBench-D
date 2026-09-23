def _fill_diagonal(shape, value):
    result = np.zeros(shape)
    np.fill_diagonal(result, value)
    return (result,)
