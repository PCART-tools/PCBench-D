    def set_visible(self, visible):
        """ Set the visibility of our artists """
        self.visible = visible
        for artist in self.artists:
            artist.set_visible(visible)
