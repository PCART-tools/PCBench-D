    @property
    def _is_numeric(self):
        from pandas.core.dtypes.common import is_object_dtype
        return not is_object_dtype(self.subtype)
