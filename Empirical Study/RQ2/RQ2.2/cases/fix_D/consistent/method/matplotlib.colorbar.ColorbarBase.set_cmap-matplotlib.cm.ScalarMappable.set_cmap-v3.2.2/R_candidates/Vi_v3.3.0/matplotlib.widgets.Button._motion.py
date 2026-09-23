    def _motion(self, event):
        if self.ignore(event):
            return
        c = self.hovercolor if event.inaxes == self.ax else self.color
        if c != self.ax.get_facecolor():
            self.ax.set_facecolor(c)
            if self.drawon:
                self.ax.figure.canvas.draw()
