    def _set_artist_props(self, a):
        if a is None:
            return
        a.set_figure(self.get_figure(root=False))
