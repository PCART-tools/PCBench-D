    def set_val(self, val):
        """
        Set slider value to *val*.

        Parameters
        ----------
        val : tuple or array-like of float
        """
        val = np.sort(np.asanyarray(val))
        if val.shape != (2,):
            raise ValueError(
                f"val must have shape (2,) but has shape {val.shape}"
            )
        val[0] = self._min_in_bounds(val[0])
        val[1] = self._max_in_bounds(val[1])
        xy = self.poly.xy
        if self.orientation == "vertical":
            xy[0] = 0, val[0]
            xy[1] = 0, val[1]
            xy[2] = 1, val[1]
            xy[3] = 1, val[0]
            xy[4] = 0, val[0]
        else:
            xy[0] = val[0], 0
            xy[1] = val[0], 1
            xy[2] = val[1], 1
            xy[3] = val[1], 0
            xy[4] = val[0], 0
        self.poly.xy = xy
        self.valtext.set_text(self._format(val))
        if self.drawon:
            self.ax.figure.canvas.draw_idle()
        self.val = val
        if self.eventson:
            self._observers.process("changed", val)
