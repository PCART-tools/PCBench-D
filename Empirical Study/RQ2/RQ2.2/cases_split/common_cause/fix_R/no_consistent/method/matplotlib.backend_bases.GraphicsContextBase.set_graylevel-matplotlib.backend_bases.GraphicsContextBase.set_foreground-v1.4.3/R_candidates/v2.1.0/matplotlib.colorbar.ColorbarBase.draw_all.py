    def draw_all(self):
        '''
        Calculate any free parameters based on the current cmap and norm,
        and do all the drawing.
        '''

        self._process_values()
        self._find_range()
        X, Y = self._mesh()
        C = self._values[:, np.newaxis]
        self._config_axes(X, Y)
        if self.filled:
            self._add_solids(X, Y, C)
