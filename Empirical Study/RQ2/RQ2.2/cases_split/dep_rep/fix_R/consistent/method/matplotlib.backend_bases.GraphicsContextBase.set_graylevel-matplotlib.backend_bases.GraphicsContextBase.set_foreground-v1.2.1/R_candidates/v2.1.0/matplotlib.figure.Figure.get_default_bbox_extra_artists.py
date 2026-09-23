    def get_default_bbox_extra_artists(self):
        bbox_artists = [artist for artist in self.get_children()
                        if artist.get_visible()]
        for ax in self.axes:
            if ax.get_visible():
                bbox_artists.extend(ax.get_default_bbox_extra_artists())
        # we don't want the figure's patch to influence the bbox calculation
        bbox_artists.remove(self.patch)
        return bbox_artists
