    @classmethod
    def _create_categorical(cls, data, dtype=None):
        """
        *this is an internal non-public method*

        create the correct categorical from data and the properties

        Parameters
        ----------
        data : data for new Categorical
        dtype : CategoricalDtype, defaults to existing

        Returns
        -------
        Categorical
        """
        if isinstance(data, (cls, ABCSeries)) and is_categorical_dtype(data):
            data = data.values

        if not isinstance(data, ABCCategorical):
            return Categorical(data, dtype=dtype)

        if isinstance(dtype, CategoricalDtype) and dtype != data.dtype:
            # we want to silently ignore dtype='category'
            data = data._set_dtype(dtype)
        return data
