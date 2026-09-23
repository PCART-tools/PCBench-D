    def onmove(self, event):
        """Internal event handler to draw the cursor when the mouse moves."""
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True

        self.linev.set_xdata((event.xdata, event.xdata))
        self.linev.set_visible(self.visible and self.vertOn)

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.lineh.set_visible(self.visible and self.horizOn)

        if self.visible and (self.vertOn or self.horizOn):
            self._update()
