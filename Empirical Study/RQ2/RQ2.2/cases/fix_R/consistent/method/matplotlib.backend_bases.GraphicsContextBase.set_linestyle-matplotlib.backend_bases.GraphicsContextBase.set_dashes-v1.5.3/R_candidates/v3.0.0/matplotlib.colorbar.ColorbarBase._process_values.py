    def _process_values(self, b=None):
        '''
        Set the :attr:`_boundaries` and :attr:`_values` attributes
        based on the input boundaries and values.  Input boundaries
        can be *self.boundaries* or the argument *b*.
        '''
        if b is None:
            b = self.boundaries
        if b is not None:
            self._boundaries = np.asarray(b, dtype=float)
            if self.values is None:
                self._values = 0.5 * (self._boundaries[:-1]
                                      + self._boundaries[1:])
                if isinstance(self.norm, colors.NoNorm):
                    self._values = (self._values + 0.00001).astype(np.int16)
                return
            self._values = np.array(self.values)
            return
        if self.values is not None:
            self._values = np.array(self.values)
            if self.boundaries is None:
                b = np.zeros(len(self.values) + 1, 'd')
                b[1:-1] = 0.5 * (self._values[:-1] - self._values[1:])
                b[0] = 2.0 * b[1] - b[2]
                b[-1] = 2.0 * b[-2] - b[-3]
                self._boundaries = b
                return
            self._boundaries = np.array(self.boundaries)
            return
        # Neither boundaries nor values are specified;
        # make reasonable ones based on cmap and norm.
        if isinstance(self.norm, colors.NoNorm):
            b = self._uniform_y(self.cmap.N + 1) * self.cmap.N - 0.5
            v = np.zeros((len(b) - 1,), dtype=np.int16)
            v[self._inside] = np.arange(self.cmap.N, dtype=np.int16)
            if self._extend_lower():
                v[0] = -1
            if self._extend_upper():
                v[-1] = self.cmap.N
            self._boundaries = b
            self._values = v
            return
        elif isinstance(self.norm, colors.BoundaryNorm):
            b = list(self.norm.boundaries)
            if self._extend_lower():
                b = [b[0] - 1] + b
            if self._extend_upper():
                b = b + [b[-1] + 1]
            b = np.array(b)
            v = np.zeros((len(b) - 1,), dtype=float)
            bi = self.norm.boundaries
            v[self._inside] = 0.5 * (bi[:-1] + bi[1:])
            if self._extend_lower():
                v[0] = b[0] - 1
            if self._extend_upper():
                v[-1] = b[-1] + 1
            self._boundaries = b
            self._values = v
            return
        else:
            if not self.norm.scaled():
                self.norm.vmin = 0
                self.norm.vmax = 1

            self.norm.vmin, self.norm.vmax = mtransforms.nonsingular(
                self.norm.vmin,
                self.norm.vmax,
                expander=0.1)

            b = self.norm.inverse(self._uniform_y(self.cmap.N + 1))

            if isinstance(self.norm, (colors.PowerNorm, colors.LogNorm)):
                # If using a lognorm or powernorm, ensure extensions don't
                # go negative
                if self._extend_lower():
                    b[0] = 0.9 * b[0]
                if self._extend_upper():
                    b[-1] = 1.1 * b[-1]
            else:
                if self._extend_lower():
                    b[0] = b[0] - 1
                if self._extend_upper():
                    b[-1] = b[-1] + 1
        self._process_values(b)
