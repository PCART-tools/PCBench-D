    def _update(self):
        self.update_from(self.patch)

        # Place the shadow patch directly behind the inherited patch.
        self.set_zorder(np.nextafter(self.patch.zorder, -np.inf))

        if self.props is not None:
            self.update(self.props)
        else:
            color = .3 * np.asarray(colors.to_rgb(self.patch.get_facecolor()))
            self.set_facecolor(color)
            self.set_edgecolor(color)
            self.set_alpha(0.5)
