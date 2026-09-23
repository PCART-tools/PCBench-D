    @classmethod
    def _concat_same_type(self, to_concat):
        from pandas.core.dtypes.concat import concat_categorical

        return concat_categorical(to_concat)
