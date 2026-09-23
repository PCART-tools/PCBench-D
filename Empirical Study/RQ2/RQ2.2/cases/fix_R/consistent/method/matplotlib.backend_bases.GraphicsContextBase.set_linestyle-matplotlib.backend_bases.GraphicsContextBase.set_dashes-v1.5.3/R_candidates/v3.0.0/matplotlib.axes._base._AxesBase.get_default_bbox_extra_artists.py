    def get_default_bbox_extra_artists(self):
        """
        Return a default list of artists that are used for the bounding box
        calculation.

        Artists are excluded either by not being visible or
        ``artist.set_in_layout(False)``.
        """
        return [artist for artist in self.get_children()
                if (artist.get_visible() and artist.get_in_layout())]
