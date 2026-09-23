    def _cast_partial_indexing_scalar(self, label):
        try:
            key = Period(label, freq=self.freq)
        except ValueError as err:
            # we cannot construct the Period
            raise KeyError(label) from err
        return key
