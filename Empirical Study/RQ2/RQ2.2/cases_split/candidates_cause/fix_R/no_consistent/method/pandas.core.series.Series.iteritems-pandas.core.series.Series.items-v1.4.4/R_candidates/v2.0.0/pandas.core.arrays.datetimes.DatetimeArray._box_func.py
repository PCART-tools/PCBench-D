    def _box_func(self, x: np.datetime64) -> Timestamp | NaTType:
        # GH#42228
        value = x.view("i8")
        ts = Timestamp._from_value_and_reso(value, reso=self._creso, tz=self.tz)
        return ts
