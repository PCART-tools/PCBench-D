    def bfill(self, axis=None, inplace=False, limit=None, downcast=None):
        """
        Synonym for :meth:`DataFrame.fillna(method='bfill') <DataFrame.fillna>`
        """
        return self.fillna(method='bfill', axis=axis, inplace=inplace,
                           limit=limit, downcast=downcast)
