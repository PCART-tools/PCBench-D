    def _recompute_path(self):
        # Inner and outer rings are connected unless the annulus is complete
        if abs((self.theta2 - self.theta1) - 360) <= 1e-12:
            theta1, theta2 = 0, 360
            connector = Path.MOVETO
        else:
            theta1, theta2 = self.theta1, self.theta2
            connector = Path.LINETO

        # Form the outer ring
        arc = Path.arc(theta1, theta2)

        if self.width is not None:
            # Partial annulus needs to draw the outer ring
            # followed by a reversed and scaled inner ring
            v1 = arc.vertices
            v2 = arc.vertices[::-1] * (self.r - self.width) / self.r
            v = np.concatenate([v1, v2, [v1[0, :], (0, 0)]])
            c = np.concatenate([
                arc.codes, arc.codes, [connector, Path.CLOSEPOLY]])
            c[len(arc.codes)] = connector
        else:
            # Wedge doesn't need an inner ring
            v = np.concatenate([
                arc.vertices, [(0, 0), arc.vertices[0, :], (0, 0)]])
            c = np.concatenate([
                arc.codes, [connector, connector, Path.CLOSEPOLY]])

        # Shift and scale the wedge to the final location.
        v *= self.r
        v += np.asarray(self.center)
        self._path = Path(v, c)
