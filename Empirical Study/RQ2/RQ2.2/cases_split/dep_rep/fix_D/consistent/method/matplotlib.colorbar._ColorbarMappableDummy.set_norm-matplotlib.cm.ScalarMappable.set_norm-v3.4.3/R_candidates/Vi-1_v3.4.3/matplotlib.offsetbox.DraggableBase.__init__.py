    def __init__(self, ref_artist, use_blit=False):
        self.ref_artist = ref_artist
        self.got_artist = False

        self.canvas = self.ref_artist.figure.canvas
        self._use_blit = use_blit and self.canvas.supports_blit

        c2 = self.canvas.mpl_connect('pick_event', self.on_pick)
        c3 = self.canvas.mpl_connect('button_release_event', self.on_release)

        if not ref_artist.pickable():
            ref_artist.set_picker(True)
        overridden_picker = _api.deprecate_method_override(
            __class__.artist_picker, self, since="3.3",
            addendum="Directly set the artist's picker if desired.")
        if overridden_picker is not None:
            ref_artist.set_picker(overridden_picker)
        self.cids = [c2, c3]
