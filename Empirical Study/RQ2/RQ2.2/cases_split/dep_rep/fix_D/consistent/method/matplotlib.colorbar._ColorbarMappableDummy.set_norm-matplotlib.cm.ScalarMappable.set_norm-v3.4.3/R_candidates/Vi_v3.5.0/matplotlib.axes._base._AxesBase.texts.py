    @property
    def texts(self):
        return self.ArtistList(self, 'texts', 'add_text',
                               valid_types=mtext.Text)
