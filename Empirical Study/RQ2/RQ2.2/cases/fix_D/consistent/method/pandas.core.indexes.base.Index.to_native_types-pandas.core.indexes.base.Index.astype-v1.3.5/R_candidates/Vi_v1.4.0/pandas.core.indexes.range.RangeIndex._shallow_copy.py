    @doc(Int64Index._shallow_copy)
    def _shallow_copy(self, values, name: Hashable = no_default):
        name = self.name if name is no_default else name

        if values.dtype.kind == "f":
            return Float64Index(values, name=name)
        return Int64Index._simple_new(values, name=name)
