    def _maybe_align_series_as_frame(self, series: Series, axis: AxisInt):
        """
        If the Series operand is not EA-dtype, we can broadcast to 2D and operate
        blockwise.
        """
        rvalues = series._values
        if not isinstance(rvalues, np.ndarray):
            # TODO(EA2D): no need to special-case with 2D EAs
            if rvalues.dtype in ("datetime64[ns]", "timedelta64[ns]"):
                # We can losslessly+cheaply cast to ndarray
                rvalues = np.asarray(rvalues)
            else:
                return series

        if axis == 0:
            rvalues = rvalues.reshape(-1, 1)
        else:
            rvalues = rvalues.reshape(1, -1)

        rvalues = np.broadcast_to(rvalues, self.shape)
        # pass dtype to avoid doing inference
        return self._constructor(
            rvalues,
            index=self.index,
            columns=self.columns,
            dtype=rvalues.dtype,
        )
