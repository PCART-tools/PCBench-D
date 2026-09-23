    def _validate_for_numeric_unaryop(self, op, opstr):
        """
        Validate if we can perform a numeric unary operation.
        """
        if not self._is_numeric_dtype:
            raise TypeError(
                "cannot evaluate a numeric op "
                "{opstr} for type: {typ}".format(opstr=opstr, typ=type(self).__name__)
            )
