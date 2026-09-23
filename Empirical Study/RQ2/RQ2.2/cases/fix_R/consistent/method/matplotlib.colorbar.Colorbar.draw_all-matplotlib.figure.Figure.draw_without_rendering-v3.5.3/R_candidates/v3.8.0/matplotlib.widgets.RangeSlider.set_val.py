    def set_val(self, val):
        """
        Set slider value to *val*.

        Parameters
        ----------
        val : tuple or array-like of float
        """
        val = np.sort(val)
        _api.check_shape((2,), val=val)
        # Reset value to allow _value_in_bounds() to work.
        self.val = (self.valmin, self.valmax)
        vmin, vmax = self._value_in_bounds(val)
        self._update_selection_poly(vmin, vmax)
        if self.orientation == "vertical":
            self._handles[0].set_ydata([vmin])
            self._handles[1].set_ydata([vmax])
        else:
            self._handles[0].set_xdata([vmin])
            self._handles[1].set_xdata([vmax])

        self.valtext.set_text(self._format((vmin, vmax)))

        if self.drawon:
            self.ax.figure.canvas.draw_idle()
        self.val = (vmin, vmax)
        if self.eventson:
            self._observers.process("changed", (vmin, vmax))
