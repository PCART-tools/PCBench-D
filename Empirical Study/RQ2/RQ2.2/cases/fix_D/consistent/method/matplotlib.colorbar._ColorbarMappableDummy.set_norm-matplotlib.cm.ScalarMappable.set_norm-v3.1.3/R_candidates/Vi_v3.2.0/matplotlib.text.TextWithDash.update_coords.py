    def update_coords(self, renderer):
        """
        Computes the actual *x*, *y* coordinates for text based on the
        input *x*, *y* and the *dashlength*. Since the rotation is
        with respect to the actual canvas's coordinates we need to map
        back and forth.
        """
        dashx, dashy = self.get_unitless_position()
        dashlength = self.get_dashlength()
        # Shortcircuit this process if we don't have a dash
        if dashlength == 0.0:
            self._x, self._y = dashx, dashy
            return

        dashrotation = self.get_dashrotation()
        dashdirection = self.get_dashdirection()
        dashpad = self.get_dashpad()
        dashpush = self.get_dashpush()

        angle = get_rotation(dashrotation)
        theta = np.pi * (angle / 180.0 + dashdirection - 1)
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)

        transform = self.get_transform()

        # Compute the dash end points
        # The 'c' prefix is for canvas coordinates
        cxy = transform.transform((dashx, dashy))
        cd = np.array([cos_theta, sin_theta])
        c1 = cxy + dashpush * cd
        c2 = cxy + (dashpush + dashlength) * cd

        inverse = transform.inverted()
        (x1, y1), (x2, y2) = inverse.transform([c1, c2])
        self.dashline.set_data((x1, x2), (y1, y2))

        # We now need to extend this vector out to
        # the center of the text area.
        # The basic problem here is that we're "rotating"
        # two separate objects but want it to appear as
        # if they're rotated together.
        # This is made non-trivial because of the
        # interaction between text rotation and alignment -
        # text alignment is based on the bbox after rotation.
        # We reset/force both alignments to 'center'
        # so we can do something relatively reasonable.
        # There's probably a better way to do this by
        # embedding all this in the object's transformations,
        # but I don't grok the transformation stuff
        # well enough yet.
        we = Text.get_window_extent(self, renderer=renderer)
        w, h = we.width, we.height
        # Watch for zeros
        if sin_theta == 0.0:
            dx = w
            dy = 0.0
        elif cos_theta == 0.0:
            dx = 0.0
            dy = h
        else:
            tan_theta = sin_theta / cos_theta
            dx = w
            dy = w * tan_theta
            if dy > h or dy < -h:
                dy = h
                dx = h / tan_theta
        cwd = np.array([dx, dy]) / 2
        cwd *= 1 + dashpad / np.sqrt(np.dot(cwd, cwd))
        cw = c2 + (dashdirection * 2 - 1) * cwd

        self._x, self._y = inverse.transform(cw)

        # Now set the window extent
        # I'm not at all sure this is the right way to do this.
        we = Text.get_window_extent(self, renderer=renderer)
        self._twd_window_extent = we.frozen()
        self._twd_window_extent.update_from_data_xy(np.array([c1]), False)

        # Finally, make text align center
        Text.set_horizontalalignment(self, 'center')
        Text.set_verticalalignment(self, 'center')
