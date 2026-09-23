    def onmove(self, event):
        axs = [ax for ax in self.axes if ax.contains(event)[0]]
        if self.ignore(event) or not axs or not event.canvas.widgetlock.available(self):
            return
        ax = cbook._topmost_artist(axs)
        xdata, ydata = ((event.xdata, event.ydata) if event.inaxes is ax
                        else ax.transData.inverted().transform((event.x, event.y)))
        for line in self.vlines:
            line.set_xdata((xdata, xdata))
            line.set_visible(self.visible and self.vertOn)
        for line in self.hlines:
            line.set_ydata((ydata, ydata))
            line.set_visible(self.visible and self.horizOn)
        if self.visible and (self.vertOn or self.horizOn):
            self._update()
