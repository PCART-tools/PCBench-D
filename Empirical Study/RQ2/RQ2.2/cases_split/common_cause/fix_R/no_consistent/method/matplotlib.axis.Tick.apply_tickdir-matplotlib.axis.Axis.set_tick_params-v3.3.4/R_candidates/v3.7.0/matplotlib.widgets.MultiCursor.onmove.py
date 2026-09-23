    def onmove(self, event):
        if (self.ignore(event)
                or event.inaxes not in self.axes
                or not event.canvas.widgetlock.available(self)):
            return
        for line in self.vlines:
            line.set_xdata((event.xdata, event.xdata))
            line.set_visible(self.visible and self.vertOn)
        for line in self.hlines:
            line.set_ydata((event.ydata, event.ydata))
            line.set_visible(self.visible and self.horizOn)
        if self.visible and (self.vertOn or self.horizOn):
            self._update()
