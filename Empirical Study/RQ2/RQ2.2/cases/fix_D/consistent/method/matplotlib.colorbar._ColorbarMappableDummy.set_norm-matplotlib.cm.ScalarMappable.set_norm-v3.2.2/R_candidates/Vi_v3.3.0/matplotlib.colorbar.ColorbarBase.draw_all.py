    def draw_all(self):
        """
        Calculate any free parameters based on the current cmap and norm,
        and do all the drawing.
        """
        # sets self._boundaries and self._values in real data units.
        # takes into account extend values:
        self._process_values()
        # sets self.vmin and vmax in data units, but just for the part of the
        # colorbar that is not part of the extend patch:
        self._find_range()
        # returns the X and Y mesh, *but* this was/is in normalized units:
        X, Y = self._mesh()
        C = self._values[:, np.newaxis]

        self._config_axis()  # Inline it after deprecation elapses.
        # Configure axes limits, patch, and outline.
        xy = self._outline(X, Y)
        xmin, ymin = xy.min(axis=0)
        xmax, ymax = xy.max(axis=0)
        self.ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        self.outline.set_xy(xy)
        self.patch.set_xy(xy)
        self.update_ticks()

        if self.filled:
            self._add_solids(X, Y, C)
