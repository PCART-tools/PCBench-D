    @_api.deprecated("3.3", alternative="self.ref_artist.contains")
    def artist_picker(self, artist, evt):
        return self.ref_artist.contains(evt)
