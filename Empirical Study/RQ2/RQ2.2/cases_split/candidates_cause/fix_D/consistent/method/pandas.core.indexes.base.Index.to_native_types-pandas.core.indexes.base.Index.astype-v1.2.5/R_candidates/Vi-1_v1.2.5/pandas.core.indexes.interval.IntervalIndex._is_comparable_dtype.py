    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        if not isinstance(dtype, IntervalDtype):
            return False
        common_subtype = find_common_type([self.dtype.subtype, dtype.subtype])
        return not is_object_dtype(common_subtype)
