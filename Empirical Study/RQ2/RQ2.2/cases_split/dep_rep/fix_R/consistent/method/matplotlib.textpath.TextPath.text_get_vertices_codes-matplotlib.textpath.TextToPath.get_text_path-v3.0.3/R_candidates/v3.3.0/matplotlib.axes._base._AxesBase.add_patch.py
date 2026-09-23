    def add_patch(self, p):
        """
        Add a `~.Patch` to the axes' patches; return the patch.
        """
        self._set_artist_props(p)
        if p.get_clip_path() is None:
            p.set_clip_path(self.patch)
        self._update_patch_limits(p)
        self.patches.append(p)
        p._remove_method = self.patches.remove
        return p
