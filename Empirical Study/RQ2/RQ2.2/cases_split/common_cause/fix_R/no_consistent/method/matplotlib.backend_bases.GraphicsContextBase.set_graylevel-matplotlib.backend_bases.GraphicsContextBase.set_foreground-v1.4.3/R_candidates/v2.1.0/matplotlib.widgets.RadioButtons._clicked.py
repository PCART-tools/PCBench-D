    def _clicked(self, event):
        if self.ignore(event):
            return
        if event.button != 1:
            return
        if event.inaxes != self.ax:
            return
        xy = self.ax.transAxes.inverted().transform_point((event.x, event.y))
        pclicked = np.array([xy[0], xy[1]])

        def inside(p):
            pcirc = np.array([p.center[0], p.center[1]])
            return dist(pclicked, pcirc) < p.radius

        for i, (p, t) in enumerate(zip(self.circles, self.labels)):
            if t.get_window_extent().contains(event.x, event.y) or inside(p):
                self.set_active(i)
                break
        else:
            return
