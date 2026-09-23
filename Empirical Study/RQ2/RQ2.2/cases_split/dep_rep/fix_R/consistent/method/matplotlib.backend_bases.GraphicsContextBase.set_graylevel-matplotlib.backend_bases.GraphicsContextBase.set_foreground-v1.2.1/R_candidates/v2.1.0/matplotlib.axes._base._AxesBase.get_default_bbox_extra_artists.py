    def get_default_bbox_extra_artists(self):
        return [artist for artist in self.get_children()
                if artist.get_visible()]
