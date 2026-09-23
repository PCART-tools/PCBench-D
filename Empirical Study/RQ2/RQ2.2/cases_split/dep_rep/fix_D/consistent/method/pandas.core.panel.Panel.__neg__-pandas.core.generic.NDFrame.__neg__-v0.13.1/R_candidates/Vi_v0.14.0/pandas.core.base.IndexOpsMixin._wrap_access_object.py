    def _wrap_access_object(self, obj):
        # we may need to coerce the input as we don't want non int64 if
        # we have an integer result
        if hasattr(obj,'dtype') and com.is_integer_dtype(obj):
            obj = obj.astype(np.int64)

        if isinstance(self, com.ABCSeries):
            return self._constructor(obj,index=self.index).__finalize__(self)

        return obj
