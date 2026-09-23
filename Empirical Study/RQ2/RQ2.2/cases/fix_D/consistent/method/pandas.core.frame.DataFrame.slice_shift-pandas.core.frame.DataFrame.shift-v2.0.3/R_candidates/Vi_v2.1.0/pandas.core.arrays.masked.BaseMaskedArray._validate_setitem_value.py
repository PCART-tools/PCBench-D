    def _validate_setitem_value(self, value):
        """
        Check if we have a scalar that we can cast losslessly.

        Raises
        ------
        TypeError
        """
        kind = self.dtype.kind
        # TODO: get this all from np_can_hold_element?
        if kind == "b":
            if lib.is_bool(value):
                return value

        elif kind == "f":
            if lib.is_integer(value) or lib.is_float(value):
                return value

        else:
            if lib.is_integer(value) or (lib.is_float(value) and value.is_integer()):
                return value
            # TODO: unsigned checks

        # Note: without the "str" here, the f-string rendering raises in
        #  py38 builds.
        raise TypeError(f"Invalid value '{str(value)}' for dtype {self.dtype}")
