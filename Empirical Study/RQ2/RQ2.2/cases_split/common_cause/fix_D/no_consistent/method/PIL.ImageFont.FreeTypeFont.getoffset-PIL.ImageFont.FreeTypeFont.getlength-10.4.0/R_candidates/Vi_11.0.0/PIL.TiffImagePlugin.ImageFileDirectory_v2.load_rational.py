    @_register_loader(5, 8)
    def load_rational(
        self, data: bytes, legacy_api: bool = True
    ) -> tuple[tuple[int, int] | IFDRational, ...]:
        vals = self._unpack(f"{len(data) // 4}L", data)

        def combine(a: int, b: int) -> tuple[int, int] | IFDRational:
            return (a, b) if legacy_api else IFDRational(a, b)

        return tuple(combine(num, denom) for num, denom in zip(vals[::2], vals[1::2]))
