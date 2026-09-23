    @staticmethod
    def _validate(data):
        if not isinstance(data.dtype, SparseDtype):
            msg = "Can only use the '.sparse' accessor with Sparse data."
            raise AttributeError(msg)
