    def set_val(self, val):
        """
        Set slider value to *val*.

        Parameters
        ----------
        val : float
        """
        if self.orientation == 'vertical':
            self.poly.set_height(val - self.poly.get_y())
            self._handle.set_ydata([val])
        else:
            self.poly.set_width(val - self.poly.get_x())
            self._handle.set_xdata([val])
        self.valtext.set_text(self._format(val))
        if self.drawon:
            self.ax.get_figure(root=True).canvas.draw_idle()
        self.val = val
        if self.eventson:
            self._observers.process('changed', val)
