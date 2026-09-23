def _indexOp(opname):
    """
    Wrapper function for index comparison operations, to avoid
    code duplication.
    """

    def wrapper(self, other):
        func = getattr(self._data.view(np.ndarray), opname)
        result = func(np.asarray(other))

        # technically we could support bool dtyped Index
        # for now just return the indexing array directly
        if is_bool_dtype(result):
            return result
        try:
            return Index(result)
        except:  # pragma: no cover
            return result
    return wrapper
