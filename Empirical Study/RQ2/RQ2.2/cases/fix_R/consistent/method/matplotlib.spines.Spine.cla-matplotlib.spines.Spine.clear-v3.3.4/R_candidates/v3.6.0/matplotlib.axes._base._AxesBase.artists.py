    @property
    def artists(self):
        return self.ArtistList(self, 'artists', 'add_artist', invalid_types=(
            mcoll.Collection, mimage.AxesImage, mlines.Line2D, mpatches.Patch,
            mtable.Table, mtext.Text))
