    @staticmethod
    def _create_categorical(self, data, categories=None, ordered=None):
        """
        *this is an internal non-public method*

        create the correct categorical from data and the properties

        Parameters
        ----------
        data : data for new Categorical
        categories : optional categories, defaults to existing
        ordered : optional ordered attribute, defaults to existing

        Returns
        -------
        Categorical
        """
        if not isinstance(data, ABCCategorical):
            ordered = False if ordered is None else ordered
            from pandas.core.categorical import Categorical
            data = Categorical(data, categories=categories, ordered=ordered)
        else:
            if categories is not None:
                data = data.set_categories(categories)
            if ordered is not None:
                data = data.set_ordered(ordered)
        return data
