    def ffill(self, axis=0, inplace=False, limit=None, downcast=None):
        "Synonym for NDFrame.fillna(method='ffill')"
        return self.fillna(method='ffill', axis=axis, inplace=inplace,
                           limit=limit, downcast=downcast)
