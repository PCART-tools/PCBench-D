    def _maybe_convert_setitem_value(self, value):
        """Maybe convert value to be pyarrow compatible."""
        # TODO: Make more robust like ArrowStringArray._maybe_convert_setitem_value
        return value
