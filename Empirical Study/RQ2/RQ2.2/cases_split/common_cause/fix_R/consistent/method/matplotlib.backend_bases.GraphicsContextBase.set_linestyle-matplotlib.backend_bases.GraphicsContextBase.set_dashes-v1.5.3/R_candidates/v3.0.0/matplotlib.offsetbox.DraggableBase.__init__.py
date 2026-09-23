    def __init__(self, ref_artist, use_blit=False):
        self.ref_artist = ref_artist
        self.got_artist = False

        self.canvas = self.ref_artist.figure.canvas
        self._use_blit = use_blit and self.canvas.supports_blit

        c2 = self.canvas.mpl_connect('pick_event', self.on_pick)
        c3 = self.canvas.mpl_connect('button_release_event', self.on_release)

        ref_artist.set_picker(self.artist_picker)
        self.cids = [c2, c3]
