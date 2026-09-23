    @property
    def texts(self):
        return self.ArtistList(self, 'texts', valid_types=mtext.Text)
