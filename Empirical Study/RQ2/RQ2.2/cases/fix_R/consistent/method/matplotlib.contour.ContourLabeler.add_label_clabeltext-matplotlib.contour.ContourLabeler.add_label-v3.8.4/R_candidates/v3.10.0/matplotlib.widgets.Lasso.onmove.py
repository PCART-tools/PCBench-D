    def onmove(self, event):
        if (self.ignore(event)
                or self.verts is None
                or event.button != 1
                or not self.ax.contains(event)[0]):
            return
        self.verts.append(self._get_data_coords(event))
        self.line.set_data(list(zip(*self.verts)))

        if self.useblit:
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
