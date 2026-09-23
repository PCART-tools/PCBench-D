    def _make_str_accessor(self):
        from pandas.core.series import Series
        from pandas.core.index import Index
        if isinstance(self, Series) and not com.is_object_dtype(self.dtype):
            # this really should exclude all series with any non-string values,
            # but that isn't practical for performance reasons until we have a
            # str dtype (GH 9343)
            raise AttributeError("Can only use .str accessor with string "
                                 "values, which use np.object_ dtype in "
                                 "pandas")
        elif isinstance(self, Index):
            # see scc/inferrence.pyx which can contain string values
            allowed_types = ('string', 'unicode', 'mixed', 'mixed-integer')
            if self.inferred_type not in allowed_types:
                message = ("Can only use .str accessor with string values "
                           "(i.e. inferred_type is 'string', 'unicode' or 'mixed')")
                raise AttributeError(message)
            if self.nlevels > 1:
                message = "Can only use .str accessor with Index, not MultiIndex"
                raise AttributeError(message)
        return StringMethods(self)
