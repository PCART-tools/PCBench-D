    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or event.inaxes != self.ax:
            return
        xy = self.ax.transAxes.inverted().transform_point((event.x, event.y))
        pclicked = np.array([xy[0], xy[1]])
        distances = {}
        for i, (p, t) in enumerate(zip(self.circles, self.labels)):
            if (t.get_window_extent().contains(event.x, event.y)
                    or np.linalg.norm(pclicked - p.center) < p.radius):
                distances[i] = np.linalg.norm(pclicked - p.center)
        if len(distances) > 0:
            closest = min(distances, key=distances.get)
            self.set_active(closest)
