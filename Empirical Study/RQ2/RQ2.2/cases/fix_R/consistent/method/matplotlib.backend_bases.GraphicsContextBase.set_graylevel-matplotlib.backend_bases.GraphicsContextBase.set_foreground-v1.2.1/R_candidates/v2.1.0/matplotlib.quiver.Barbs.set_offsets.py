    def set_offsets(self, xy):
        """
        Set the offsets for the barb polygons.  This saves the offsets passed
        in and actually sets version masked as appropriate for the existing
        U/V data. *offsets* should be a sequence.

        ACCEPTS: sequence of pairs of floats
        """
        self.x = xy[:, 0]
        self.y = xy[:, 1]
        x, y, u, v = delete_masked_points(self.x.ravel(), self.y.ravel(),
                                          self.u, self.v)
        _check_consistent_shapes(x, y, u, v)
        xy = np.hstack((x[:, np.newaxis], y[:, np.newaxis]))
        mcollections.PolyCollection.set_offsets(self, xy)
        self.stale = True
