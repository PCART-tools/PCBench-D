    @property
    def texts(self):
        return self.ArtistList(self, 'texts', 'add_artist',
                               valid_types=mtext.Text)
