    def add_label(self, x, y, rotation, lev, cvalue):
        """Add a contour label, respecting whether *use_clabeltext* was set."""
        data_x, data_y = self.axes.transData.inverted().transform((x, y))
        t = Text(
            data_x, data_y,
            text=self.get_text(lev, self.labelFmt),
            rotation=rotation,
            horizontalalignment='center', verticalalignment='center',
            zorder=self._clabel_zorder,
            color=self.labelMappable.to_rgba(cvalue, alpha=self.get_alpha()),
            fontproperties=self._label_font_props,
            clip_box=self.axes.bbox)
        if self._use_clabeltext:
            data_rotation, = self.axes.transData.inverted().transform_angles(
                [rotation], [[x, y]])
            t.set(rotation=data_rotation, transform_rotates_text=True)
        self.labelTexts.append(t)
        self.labelCValues.append(cvalue)
        self.labelXYs.append((x, y))
        # Add label to plot here - useful for manual mode label selection
        self.axes.add_artist(t)
