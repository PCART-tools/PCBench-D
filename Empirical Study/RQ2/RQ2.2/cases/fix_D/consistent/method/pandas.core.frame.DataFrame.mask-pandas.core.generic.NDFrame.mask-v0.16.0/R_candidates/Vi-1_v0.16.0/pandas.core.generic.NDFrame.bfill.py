    def bfill(self, axis=None, inplace=False, limit=None, downcast=None):
        "Synonym for NDFrame.fillna(method='bfill')"
        return self.fillna(method='bfill', axis=axis, inplace=inplace,
                           limit=limit, downcast=downcast)
