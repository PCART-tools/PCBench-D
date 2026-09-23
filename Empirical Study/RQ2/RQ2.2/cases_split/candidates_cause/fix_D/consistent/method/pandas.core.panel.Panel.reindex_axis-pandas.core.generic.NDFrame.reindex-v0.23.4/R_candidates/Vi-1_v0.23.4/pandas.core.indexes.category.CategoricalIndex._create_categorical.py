    @staticmethod
    def _create_categorical(self, data, categories=None, ordered=None,
                            dtype=None):
        """
        *this is an internal non-public method*

        create the correct categorical from data and the properties

        Parameters
        ----------
        data : data for new Categorical
        categories : optional categories, defaults to existing
        ordered : optional ordered attribute, defaults to existing
        dtype : CategoricalDtype, defaults to existing

        Returns
        -------
        Categorical
        """
        if (isinstance(data, (ABCSeries, type(self))) and
                is_categorical_dtype(data)):
            data = data.values

        if not isinstance(data, ABCCategorical):
            if ordered is None and dtype is None:
                ordered = False
            from pandas.core.arrays import Categorical
            data = Categorical(data, categories=categories, ordered=ordered,
                               dtype=dtype)
        else:
            if categories is not None:
                data = data.set_categories(categories, ordered=ordered)
            elif ordered is not None and ordered != data.ordered:
                data = data.set_ordered(ordered)
            if isinstance(dtype, CategoricalDtype):
                # we want to silently ignore dtype='category'
                data = data._set_dtype(dtype)
        return data
