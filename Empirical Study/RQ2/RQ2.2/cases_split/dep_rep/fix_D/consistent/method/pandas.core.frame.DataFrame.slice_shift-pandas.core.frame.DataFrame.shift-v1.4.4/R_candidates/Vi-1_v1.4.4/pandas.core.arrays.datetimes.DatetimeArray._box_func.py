    def _box_func(self, x) -> Timestamp | NaTType:
        if isinstance(x, np.datetime64):
            # GH#42228
            # Argument 1 to "signedinteger" has incompatible type "datetime64";
            # expected "Union[SupportsInt, Union[str, bytes], SupportsIndex]"
            x = np.int64(x)  # type: ignore[arg-type]
        ts = Timestamp(x, tz=self.tz)
        # Non-overlapping identity check (left operand type: "Timestamp",
        # right operand type: "NaTType")
        if ts is not NaT:  # type: ignore[comparison-overlap]
            # GH#41586
            # do this instead of passing to the constructor to avoid FutureWarning
            ts._set_freq(self.freq)
        return ts
