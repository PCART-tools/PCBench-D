    def _get_unique_index(self, dropna=False):
        """
        wrap Index._get_unique_index to handle NaT
        """
        res = super()._get_unique_index(dropna=dropna)
        if dropna:
            res = res.dropna()
        return res
