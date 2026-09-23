    def __eq__(self, other):
        if isinstance(other, str):
            return other.lower() in (self.name.lower(), str(self).lower())
        elif not isinstance(other, IntervalDtype):
            return False
        elif self.subtype is None or other.subtype is None:
            # None should match any subtype
            return True
        else:
            from pandas.core.dtypes.common import is_dtype_equal

            return is_dtype_equal(self.subtype, other.subtype)
