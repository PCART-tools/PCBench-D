    def draw_all(self):
        """
        Calculate any free parameters based on the current cmap and norm,
        and do all the drawing.
        """
        self._config_axis()  # Inline it after deprecation elapses.
        # Set self._boundaries and self._values, including extensions.
        self._process_values()
        # Set self.vmin and self.vmax to first and last boundary, excluding
        # extensions.
        self.vmin, self.vmax = self._boundaries[self._inside][[0, -1]]
        # Compute the X/Y mesh.
        X, Y = self._mesh()
        # Extract bounding polygon (the last entry's value (X[0, 1]) doesn't
        # matter, it just matches the CLOSEPOLY code).
        x = np.concatenate([X[[0, 1, -2, -1], 0], X[[-1, -2, 1, 0, 0], 1]])
        y = np.concatenate([Y[[0, 1, -2, -1], 0], Y[[-1, -2, 1, 0, 0], 1]])
        xy = np.column_stack([x, y])
        # Configure axes limits, patch, and outline.
        xmin, ymin = xy.min(axis=0)
        xmax, ymax = xy.max(axis=0)
        self.ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        self.outline.set_xy(xy)
        self.patch.set_xy(xy)
        self.update_ticks()
        if self.filled:
            self._add_solids(X, Y, self._values[:, np.newaxis])
