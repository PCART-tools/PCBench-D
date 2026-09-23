    def _maybe_convert_setitem_value(self, value):
        """Maybe convert value to be pyarrow compatible."""
        try:
            value = self._box_pa(value, self._pa_array.type)
        except pa.ArrowTypeError as err:
            msg = f"Invalid value '{str(value)}' for dtype {self.dtype}"
            raise TypeError(msg) from err
        return value
