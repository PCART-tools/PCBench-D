    def ffill(self, axis=None, inplace=False, limit=None, downcast=None):
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='ffill'``.

        Returns
        -------
        %(klass)s
            Object with missing values filled.
        """
        return self.fillna(
            method="ffill", axis=axis, inplace=inplace, limit=limit, downcast=downcast
        )
