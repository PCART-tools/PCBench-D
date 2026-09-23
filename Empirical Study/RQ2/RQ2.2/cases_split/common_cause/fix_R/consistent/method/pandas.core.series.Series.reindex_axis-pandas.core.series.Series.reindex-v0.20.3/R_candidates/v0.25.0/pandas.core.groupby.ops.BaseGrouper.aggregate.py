    def aggregate(self, values, how, axis=0, min_count=-1):
        return self._cython_operation(
            "aggregate", values, how, axis, min_count=min_count
        )
