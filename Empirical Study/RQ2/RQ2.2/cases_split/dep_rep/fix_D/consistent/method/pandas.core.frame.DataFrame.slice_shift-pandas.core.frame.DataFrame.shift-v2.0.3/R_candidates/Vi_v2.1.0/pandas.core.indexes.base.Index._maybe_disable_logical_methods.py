    @final
    def _maybe_disable_logical_methods(self, opname: str_t) -> None:
        """
        raise if this Index subclass does not support any or all.
        """
        if (
            isinstance(self, ABCMultiIndex)
            # TODO(3.0): PeriodArray and DatetimeArray any/all will raise,
            #  so checking needs_i8_conversion will be unnecessary
            or (needs_i8_conversion(self.dtype) and self.dtype.kind != "m")
        ):
            # This call will raise
            make_invalid_op(opname)(self)
