    @_register_writer(5)
    def write_rational(self, *values: IFDRational) -> bytes:
        return b"".join(
            self._pack("2L", *_limit_rational(frac, 2**32 - 1)) for frac in values
        )
