    @doc(Index._shallow_copy)
    def _shallow_copy(self, values=None, name: Label = lib.no_default):
        if values is not None and not self._can_hold_na and values.dtype.kind == "f":
            name = self.name if name is lib.no_default else name
            # Ensure we are not returning an Int64Index with float data:
            return Float64Index._simple_new(values, name=name)
        return super()._shallow_copy(values=values, name=name)
