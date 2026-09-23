    def _make_str_accessor(self):
        if not com.is_object_dtype(self.dtype):
            # this really should exclude all series with any non-string values,
            # but that isn't practical for performance reasons until we have a
            # str dtype (GH 9343)
            raise AttributeError("Can only use .str accessor with string "
                                 "values, which use np.object_ dtype in "
                                 "pandas")
        return StringMethods(self)
