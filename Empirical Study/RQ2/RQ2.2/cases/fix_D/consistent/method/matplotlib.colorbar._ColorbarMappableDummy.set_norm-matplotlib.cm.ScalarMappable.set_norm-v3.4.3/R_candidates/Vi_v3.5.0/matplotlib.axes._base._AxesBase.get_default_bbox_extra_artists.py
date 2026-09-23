    def get_default_bbox_extra_artists(self):
        """
        Return a default list of artists that are used for the bounding box
        calculation.

        Artists are excluded either by not being visible or
        ``artist.set_in_layout(False)``.
        """

        artists = self.get_children()

        if not (self.axison and self._frameon):
            # don't do bbox on spines if frame not on.
            for spine in self.spines.values():
                artists.remove(spine)

        if not self.axison:
            for _axis in self._get_axis_list():
                artists.remove(_axis)

        artists.remove(self.title)
        artists.remove(self._left_title)
        artists.remove(self._right_title)

        return [artist for artist in artists
                if (artist.get_visible() and artist.get_in_layout())]
