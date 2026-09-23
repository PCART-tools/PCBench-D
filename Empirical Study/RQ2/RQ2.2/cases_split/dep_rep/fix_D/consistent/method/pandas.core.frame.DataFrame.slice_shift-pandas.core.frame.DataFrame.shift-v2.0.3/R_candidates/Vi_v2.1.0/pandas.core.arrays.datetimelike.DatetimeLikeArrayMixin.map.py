    @ravel_compat
    def map(self, mapper, na_action=None):
        from pandas import Index

        result = map_array(self, mapper, na_action=na_action)
        result = Index(result)

        if isinstance(result, ABCMultiIndex):
            return result.to_numpy()
        else:
            return result.array
