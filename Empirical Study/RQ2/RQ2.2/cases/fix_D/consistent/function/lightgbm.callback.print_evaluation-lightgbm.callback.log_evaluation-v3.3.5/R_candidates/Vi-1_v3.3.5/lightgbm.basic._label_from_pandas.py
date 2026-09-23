def _label_from_pandas(label):
    if isinstance(label, pd_DataFrame):
        if len(label.columns) > 1:
            raise ValueError('DataFrame for label cannot have multiple columns')
        if _get_bad_pandas_dtypes(label.dtypes):
            raise ValueError('DataFrame.dtypes for label must be int, float or bool')
        label = np.ravel(label.values.astype(np.float32, copy=False))
    return label
