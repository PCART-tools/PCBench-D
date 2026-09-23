    def _motion(self, event):
        if self.ignore(event):
            return
        if event.inaxes == self.ax:
            c = self.hovercolor
        else:
            c = self.color
        if c != self._lastcolor:
            self.ax.set_facecolor(c)
            self._lastcolor = c
            if self.drawon:
                self.ax.figure.canvas.draw()
