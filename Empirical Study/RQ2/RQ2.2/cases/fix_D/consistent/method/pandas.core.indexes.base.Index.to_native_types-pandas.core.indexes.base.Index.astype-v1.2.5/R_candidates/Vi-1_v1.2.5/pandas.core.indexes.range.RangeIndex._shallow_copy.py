    @doc(Int64Index._shallow_copy)
    def _shallow_copy(self, values=None, name: Label = no_default):
        name = self.name if name is no_default else name

        if values is not None:
            if values.dtype.kind == "f":
                return Float64Index(values, name=name)
            return Int64Index._simple_new(values, name=name)

        result = self._simple_new(self._range, name=name)
        result._cache = self._cache
        return result
