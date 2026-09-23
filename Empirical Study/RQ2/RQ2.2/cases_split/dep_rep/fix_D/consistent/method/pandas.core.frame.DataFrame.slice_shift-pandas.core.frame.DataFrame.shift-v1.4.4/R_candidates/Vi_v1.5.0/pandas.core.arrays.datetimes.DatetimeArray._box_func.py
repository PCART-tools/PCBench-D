    def _box_func(self, x: np.datetime64) -> Timestamp | NaTType:
        # GH#42228
        value = x.view("i8")
        ts = Timestamp._from_value_and_reso(value, reso=self._reso, tz=self.tz)
        # Non-overlapping identity check (left operand type: "Timestamp",
        # right operand type: "NaTType")
        if ts is not NaT:  # type: ignore[comparison-overlap]
            # GH#41586
            # do this instead of passing to the constructor to avoid FutureWarning
            ts._set_freq(self.freq)
        return ts
