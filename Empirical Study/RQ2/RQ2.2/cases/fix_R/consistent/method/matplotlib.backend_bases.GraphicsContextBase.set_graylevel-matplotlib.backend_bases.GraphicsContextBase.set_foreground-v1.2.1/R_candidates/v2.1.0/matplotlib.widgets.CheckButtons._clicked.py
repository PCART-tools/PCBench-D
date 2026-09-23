    def _clicked(self, event):
        if self.ignore(event):
            return
        if event.button != 1:
            return
        if event.inaxes != self.ax:
            return

        for i, (p, t) in enumerate(zip(self.rectangles, self.labels)):
            if (t.get_window_extent().contains(event.x, event.y) or
                    p.get_window_extent().contains(event.x, event.y)):
                self.set_active(i)
                break
        else:
            return
