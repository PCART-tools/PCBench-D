    def ffill(self, axis=None, inplace=False, limit=None, downcast=None):
        """
        Synonym for :meth:`DataFrame.fillna` with ``method='ffill'``.
        """
        return self.fillna(method='ffill', axis=axis, inplace=inplace,
                           limit=limit, downcast=downcast)
