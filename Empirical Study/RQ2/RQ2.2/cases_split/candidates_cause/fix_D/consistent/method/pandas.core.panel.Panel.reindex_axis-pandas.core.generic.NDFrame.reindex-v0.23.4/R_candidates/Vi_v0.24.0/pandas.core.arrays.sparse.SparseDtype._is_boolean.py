    @property
    def _is_boolean(self):
        from pandas.core.dtypes.common import is_bool_dtype
        return is_bool_dtype(self.subtype)
