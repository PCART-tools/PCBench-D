    def draw_all(self):
        '''
        Calculate any free parameters based on the current cmap and norm,
        and do all the drawing.
        '''
        # sets self._boundaries and self._values in real data units.
        # takes into account extend values:
        self._process_values()
        # sets self.vmin and vmax in data units, but just for
        # the part of the colorbar that is not part of the extend
        # patch:
        self._find_range()
        # returns the X and Y mesh, *but* this was/is in normalized
        # units:
        X, Y = self._mesh()
        C = self._values[:, np.newaxis]
        # decide minor/major axis
        self.config_axis()
        self._config_axes(X, Y)
        if self.filled:
            self._add_solids(X, Y, C)
