    @_register_writer(10)
    def write_signed_rational(self, *values):
        return b"".join(
            self._pack("2l", *_limit_signed_rational(frac, 2**31 - 1, -(2**31)))
            for frac in values
        )
