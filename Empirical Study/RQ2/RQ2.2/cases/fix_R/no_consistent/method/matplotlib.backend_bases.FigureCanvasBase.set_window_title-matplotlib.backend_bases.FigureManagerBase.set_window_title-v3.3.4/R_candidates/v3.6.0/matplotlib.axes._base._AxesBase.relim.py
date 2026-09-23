    def relim(self, visible_only=False):
        """
        Recompute the data limits based on current artists.

        At present, `.Collection` instances are not supported.

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

        for artist in self._children:
            if not visible_only or artist.get_visible():
                if isinstance(artist, mlines.Line2D):
                    self._update_line_limits(artist)
                elif isinstance(artist, mpatches.Patch):
                    self._update_patch_limits(artist)
                elif isinstance(artist, mimage.AxesImage):
                    self._update_image_limits(artist)
