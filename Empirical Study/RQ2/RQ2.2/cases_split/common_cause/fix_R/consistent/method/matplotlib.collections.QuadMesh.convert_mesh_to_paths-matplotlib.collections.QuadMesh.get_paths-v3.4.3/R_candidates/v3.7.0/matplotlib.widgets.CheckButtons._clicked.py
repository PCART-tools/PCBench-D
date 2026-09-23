    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or event.inaxes != self.ax:
            return
        pclicked = self.ax.transAxes.inverted().transform((event.x, event.y))
        distances = {}
        if hasattr(self, "_rectangles"):
            for i, (p, t) in enumerate(zip(self._rectangles, self.labels)):
                x0, y0 = p.get_xy()
                if (t.get_window_extent().contains(event.x, event.y)
                        or (x0 <= pclicked[0] <= x0 + p.get_width()
                            and y0 <= pclicked[1] <= y0 + p.get_height())):
                    distances[i] = np.linalg.norm(pclicked - p.get_center())
        else:
            _, frame_inds = self._frames.contains(event)
            coords = self._frames.get_offset_transform().transform(
                self._frames.get_offsets()
            )
            for i, t in enumerate(self.labels):
                if (i in frame_inds["ind"]
                        or t.get_window_extent().contains(event.x, event.y)):
                    distances[i] = np.linalg.norm(pclicked - coords[i])
        if len(distances) > 0:
            closest = min(distances, key=distances.get)
            self.set_active(closest)
