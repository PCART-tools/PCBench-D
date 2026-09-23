    @_register_loader(10, 8)
    def load_signed_rational(self, data, legacy_api=True):
        vals = self._unpack(f"{len(data) // 4}l", data)

        def combine(a, b):
            return (a, b) if legacy_api else IFDRational(a, b)

        return tuple(combine(num, denom) for num, denom in zip(vals[::2], vals[1::2]))
