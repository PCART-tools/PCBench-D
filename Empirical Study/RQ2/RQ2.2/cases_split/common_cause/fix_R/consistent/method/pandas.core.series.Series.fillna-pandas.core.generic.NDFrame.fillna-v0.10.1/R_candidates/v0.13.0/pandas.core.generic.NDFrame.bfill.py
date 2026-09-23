    def bfill(self, axis=0, inplace=False, limit=None, downcast=None):
        "Synonym for NDFrame.fillna(method='bfill')"
        return self.fillna(method='bfill', axis=axis, inplace=inplace,
                           limit=limit, downcast=downcast)
