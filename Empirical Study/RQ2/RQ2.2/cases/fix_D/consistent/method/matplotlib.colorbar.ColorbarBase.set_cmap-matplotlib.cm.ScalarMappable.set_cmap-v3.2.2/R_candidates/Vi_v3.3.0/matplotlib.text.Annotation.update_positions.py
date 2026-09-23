    def update_positions(self, renderer):
        """
        Update the pixel positions of the annotation text and the arrow patch.
        """
        x1, y1 = self._get_position_xy(renderer)  # Annotated position.
        # generate transformation,
        self.set_transform(self._get_xy_transform(renderer, self.anncoords))

        if self.arrowprops is None:
            return

        bbox = Text.get_window_extent(self, renderer)

        d = self.arrowprops.copy()
        ms = d.pop("mutation_scale", self.get_size())
        self.arrow_patch.set_mutation_scale(ms)

        if "arrowstyle" not in d:
            # Approximately simulate the YAArrow.
            # Pop its kwargs:
            shrink = d.pop('shrink', 0.0)
            width = d.pop('width', 4)
            headwidth = d.pop('headwidth', 12)
            # Ignore frac--it is useless.
            frac = d.pop('frac', None)
            if frac is not None:
                cbook._warn_external(
                    "'frac' option in 'arrowprops' is no longer supported;"
                    " use 'headlength' to set the head length in points.")
            headlength = d.pop('headlength', 12)

            # NB: ms is in pts
            stylekw = dict(head_length=headlength / ms,
                           head_width=headwidth / ms,
                           tail_width=width / ms)

            self.arrow_patch.set_arrowstyle('simple', **stylekw)

            # using YAArrow style:
            # pick the corner of the text bbox closest to annotated point.
            xpos = [(bbox.x0, 0), ((bbox.x0 + bbox.x1) / 2, 0.5), (bbox.x1, 1)]
            ypos = [(bbox.y0, 0), ((bbox.y0 + bbox.y1) / 2, 0.5), (bbox.y1, 1)]
            x, relposx = min(xpos, key=lambda v: abs(v[0] - x1))
            y, relposy = min(ypos, key=lambda v: abs(v[0] - y1))
            self._arrow_relpos = (relposx, relposy)
            r = np.hypot(y - y1, x - x1)
            shrink_pts = shrink * r / renderer.points_to_pixels(1)
            self.arrow_patch.shrinkA = self.arrow_patch.shrinkB = shrink_pts

        # adjust the starting point of the arrow relative to the textbox.
        # TODO : Rotation needs to be accounted.
        relposx, relposy = self._arrow_relpos
        x0 = bbox.x0 + bbox.width * relposx
        y0 = bbox.y0 + bbox.height * relposy

        # The arrow will be drawn from (x0, y0) to (x1, y1). It will be first
        # clipped by patchA and patchB.  Then it will be shrunk by shrinkA and
        # shrinkB (in points).  If patch A is not set, self.bbox_patch is used.
        self.arrow_patch.set_positions((x0, y0), (x1, y1))

        if "patchA" in d:
            self.arrow_patch.set_patchA(d.pop("patchA"))
        else:
            if self._bbox_patch:
                self.arrow_patch.set_patchA(self._bbox_patch)
            else:
                if self.get_text() == "":
                    self.arrow_patch.set_patchA(None)
                    return
                pad = renderer.points_to_pixels(4)
                r = Rectangle(xy=(bbox.x0 - pad / 2, bbox.y0 - pad / 2),
                              width=bbox.width + pad, height=bbox.height + pad,
                              transform=IdentityTransform(), clip_on=False)
                self.arrow_patch.set_patchA(r)
