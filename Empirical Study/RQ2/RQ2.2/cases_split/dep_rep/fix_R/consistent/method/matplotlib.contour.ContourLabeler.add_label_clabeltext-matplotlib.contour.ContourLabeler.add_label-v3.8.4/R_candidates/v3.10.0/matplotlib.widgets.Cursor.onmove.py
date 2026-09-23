    def onmove(self, event):
        """Internal event handler to draw the cursor when the mouse moves."""
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if not self.ax.contains(event)[0]:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)
            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        xdata, ydata = self._get_data_coords(event)
        self.linev.set_xdata((xdata, xdata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_ydata((ydata, ydata))
        self.lineh.set_visible(self.visible and self.horizOn)
        if not (self.visible and (self.vertOn or self.horizOn)):
            return
        # Redraw.
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
