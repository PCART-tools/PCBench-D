    def bfill(self, axis=None, inplace=False, limit=None, downcast=None):
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='bfill'``.

        Returns
        -------
        %(klass)s
            Object with missing values filled.
        """
        return self.fillna(
            method="bfill", axis=axis, inplace=inplace, limit=limit, downcast=downcast
        )
