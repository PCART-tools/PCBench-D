    @classmethod
    def _simple_new(cls, data, sp_index, fill_value):
        if not isinstance(sp_index, SparseIndex):
            # caller must pass SparseIndex
            raise ValueError('sp_index must be a SparseIndex')

        if fill_value is None:
            if sp_index.ngaps > 0:
                # has missing hole
                fill_value = np.nan
            else:
                fill_value = na_value_for_dtype(data.dtype)

        if (is_integer_dtype(data) and is_float(fill_value) and
                sp_index.ngaps > 0):
            # if float fill_value is being included in dense repr,
            # convert values to float
            data = data.astype(float)

        result = data.view(cls)

        if not isinstance(sp_index, SparseIndex):
            # caller must pass SparseIndex
            raise ValueError('sp_index must be a SparseIndex')

        result.sp_index = sp_index
        result._fill_value = fill_value
        return result
