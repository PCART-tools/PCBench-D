    def set_UVC(self, U, V, C=None):
        self.u = ma.masked_invalid(U, copy=False).ravel()
        self.v = ma.masked_invalid(V, copy=False).ravel()
        if C is not None:
            c = ma.masked_invalid(C, copy=False).ravel()
            x, y, u, v, c = delete_masked_points(self.x.ravel(),
                                                 self.y.ravel(),
                                                 self.u, self.v, c)
            _check_consistent_shapes(x, y, u, v, c)
        else:
            x, y, u, v = delete_masked_points(self.x.ravel(), self.y.ravel(),
                                              self.u, self.v)
            _check_consistent_shapes(x, y, u, v)

        magnitude = np.hypot(u, v)
        flags, barbs, halves, empty = self._find_tails(magnitude,
                                                       self.rounding,
                                                       **self.barb_increments)

        # Get the vertices for each of the barbs

        plot_barbs = self._make_barbs(u, v, flags, barbs, halves, empty,
                                      self._length, self._pivot, self.sizes,
                                      self.fill_empty, self.flip)
        self.set_verts(plot_barbs)

        # Set the color array
        if C is not None:
            self.set_array(c)

        # Update the offsets in case the masked data changed
        xy = np.hstack((x[:, np.newaxis], y[:, np.newaxis]))
        self._offsets = xy
        self.stale = True
