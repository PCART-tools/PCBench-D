    def __init__(self, values, placement, ndim=None):
        # Ensure that we have the underlying SparseArray here...
        if isinstance(values, ABCSeries):
            values = values.values
        assert isinstance(values, SparseArray)
        super(SparseBlock, self).__init__(values, placement, ndim=ndim)
