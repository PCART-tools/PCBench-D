    def __invert__(self) -> Self:
        # This is a bit wise op for integer types
        if pa.types.is_integer(self._pa_array.type):
            return type(self)(pc.bit_wise_not(self._pa_array))
        else:
            return type(self)(pc.invert(self._pa_array))
