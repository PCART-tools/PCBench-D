    def _set_categories(self, categories, fastpath=False):
        """ Sets new categories

        Parameters
        ----------
        fastpath : boolean (default: False)
           Don't perform validation of the categories for uniqueness or nulls

        """

        categories = self._validate_categories(categories, fastpath=fastpath)
        if (not fastpath and self._categories is not None and
                len(categories) != len(self._categories)):
            raise ValueError("new categories need to have the same number of "
                             "items than the old categories!")

        self._categories = categories
