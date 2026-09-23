    @classmethod
    def _concat_same_type(self, to_concat):
        from pandas.core.dtypes.concat import _concat_categorical

        return _concat_categorical(to_concat)
