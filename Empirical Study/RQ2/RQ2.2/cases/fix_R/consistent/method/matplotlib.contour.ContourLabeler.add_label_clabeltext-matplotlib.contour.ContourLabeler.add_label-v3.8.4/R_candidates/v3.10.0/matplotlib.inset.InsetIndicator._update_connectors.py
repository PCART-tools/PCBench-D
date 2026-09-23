    def _update_connectors(self):
        (x, y) = self._rectangle.get_xy()
        width = self._rectangle.get_width()
        height = self._rectangle.get_height()

        existing_connectors = self._connectors or [None] * 4

        # connect the inset_axes to the rectangle
        for xy_inset_ax, existing in zip([(0, 0), (0, 1), (1, 0), (1, 1)],
                                         existing_connectors):
            # inset_ax positions are in axes coordinates
            # The 0, 1 values define the four edges if the inset_ax
            # lower_left, upper_left, lower_right upper_right.
            ex, ey = xy_inset_ax
            if self.axes.xaxis.get_inverted():
                ex = 1 - ex
            if self.axes.yaxis.get_inverted():
                ey = 1 - ey
            xy_data = x + ex * width, y + ey * height
            if existing is None:
                # Create new connection patch with styles inherited from the
                # parent artist.
                p = ConnectionPatch(
                    xyA=xy_inset_ax, coordsA=self._inset_ax.transAxes,
                    xyB=xy_data, coordsB=self.axes.transData,
                    arrowstyle="-",
                    edgecolor=self._edgecolor, alpha=self.get_alpha(),
                    linestyle=self._linestyle, linewidth=self._linewidth)
                self._connectors.append(p)
            else:
                # Only update positioning of existing connection patch.  We
                # do not want to override any style settings made by the user.
                existing.xy1 = xy_inset_ax
                existing.xy2 = xy_data
                existing.coords1 = self._inset_ax.transAxes
                existing.coords2 = self.axes.transData

        if existing is None:
            # decide which two of the lines to keep visible....
            pos = self._inset_ax.get_position()
            bboxins = pos.transformed(self.get_figure(root=False).transSubfigure)
            rectbbox = transforms.Bbox.from_bounds(x, y, width, height).transformed(
                self._rectangle.get_transform())
            x0 = rectbbox.x0 < bboxins.x0
            x1 = rectbbox.x1 < bboxins.x1
            y0 = rectbbox.y0 < bboxins.y0
            y1 = rectbbox.y1 < bboxins.y1
            self._connectors[0].set_visible(x0 ^ y0)
            self._connectors[1].set_visible(x0 == y1)
            self._connectors[2].set_visible(x1 == y0)
            self._connectors[3].set_visible(x1 ^ y1)
