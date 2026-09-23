    def _coerce_values(self, values):
        # asi8 is a view, needs copy
        return _block_shape(values.view("i8"), ndim=self.ndim)
