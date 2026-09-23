    def get_transform(self):
        ax = self.axes
        (x1, y1), (x2, y2) = ax.transScale.transform([*zip(*self.get_data())])
        dx = x2 - x1
        dy = y2 - y1
        if np.allclose(x1, x2):
            if np.allclose(y1, y2):
                raise ValueError(
                    f"Cannot draw a line through two identical points "
                    f"(x={self.get_xdata()}, y={self.get_ydata()})")
            # First send y1 to 0 and y2 to 1.
            return (Affine2D.from_values(1, 0, 0, 1 / dy, 0, -y1 / dy)
                    + ax.get_xaxis_transform(which="grid"))
        if np.allclose(y1, y2):
            # First send x1 to 0 and x2 to 1.
            return (Affine2D.from_values(1 / dx, 0, 0, 1, -x1 / dx, 0)
                    + ax.get_yaxis_transform(which="grid"))
        (vxlo, vylo), (vxhi, vyhi) = ax.transScale.transform(ax.viewLim)
        # General case: find intersections with view limits in either
        # direction, and draw between the middle two points.
        _, start, stop, _ = sorted([
            (vxlo, y1 + (vxlo - x1) * dy / dx),
            (vxhi, y1 + (vxhi - x1) * dy / dx),
            (x1 + (vylo - y1) * dx / dy, vylo),
            (x1 + (vyhi - y1) * dx / dy, vyhi),
        ])
        return (BboxTransformFrom(Bbox([*zip(*self.get_data())]))
                + BboxTransformTo(Bbox([start, stop]))
                + ax.transLimits + ax.transAxes)
