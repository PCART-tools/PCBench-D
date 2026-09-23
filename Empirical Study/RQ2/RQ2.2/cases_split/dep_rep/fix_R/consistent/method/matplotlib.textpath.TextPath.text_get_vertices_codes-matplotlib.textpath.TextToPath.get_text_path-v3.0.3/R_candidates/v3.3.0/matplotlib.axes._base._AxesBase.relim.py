    def relim(self, visible_only=False):
        """
        Recompute the data limits based on current artists.

        At present, `~.Collection` instances are not supported.

        Parameters
        ----------
        visible_only : bool, default: False
            Whether to exclude invisible artists.
        """
        # Collections are deliberately not supported (yet); see
        # the TODO note in artists.py.
        self.dataLim.ignore(True)
        self.dataLim.set_points(mtransforms.Bbox.null().get_points())
        self.ignore_existing_data_limits = True

        for line in self.lines:
            if not visible_only or line.get_visible():
                self._update_line_limits(line)

        for p in self.patches:
            if not visible_only or p.get_visible():
                self._update_patch_limits(p)

        for image in self.images:
            if not visible_only or image.get_visible():
                self._update_image_limits(image)
