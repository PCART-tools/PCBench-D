    @property
    def _is_boolean(self) -> bool:
        from pandas.core.dtypes.common import is_bool_dtype

        return is_bool_dtype(self.categories)
