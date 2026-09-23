    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or not self.ax.contains(event)[0]:
            return
        pclicked = self.ax.transAxes.inverted().transform((event.x, event.y))
        _, inds = self._buttons.contains(event)
        coords = self._buttons.get_offset_transform().transform(
            self._buttons.get_offsets())
        distances = {}
        if hasattr(self, "_circles"):  # Remove once circles is removed.
            for i, (p, t) in enumerate(zip(self._circles, self.labels)):
                if (t.get_window_extent().contains(event.x, event.y)
                        or np.linalg.norm(pclicked - p.center) < p.radius):
                    distances[i] = np.linalg.norm(pclicked - p.center)
        else:
            for i, t in enumerate(self.labels):
                if (i in inds["ind"]
                        or t.get_window_extent().contains(event.x, event.y)):
                    distances[i] = np.linalg.norm(pclicked - coords[i])
        if len(distances) > 0:
            closest = min(distances, key=distances.get)
            self.set_active(closest)
