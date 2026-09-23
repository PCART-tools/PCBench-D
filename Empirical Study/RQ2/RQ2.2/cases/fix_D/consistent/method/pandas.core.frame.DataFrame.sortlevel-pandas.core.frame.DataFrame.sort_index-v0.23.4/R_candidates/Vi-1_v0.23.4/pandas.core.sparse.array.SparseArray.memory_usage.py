    @Appender(IndexOpsMixin.memory_usage.__doc__)
    def memory_usage(self, deep=False):
        values = self.sp_values

        v = values.nbytes

        if deep and is_object_dtype(self) and not PYPY:
            v += lib.memory_usage_of_objects(values)

        return v
