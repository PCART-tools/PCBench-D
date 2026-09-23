    @classmethod
    def _concat_same_type(self, to_concat):
        from pandas.core.dtypes.concat import union_categoricals

        return union_categoricals(to_concat)
