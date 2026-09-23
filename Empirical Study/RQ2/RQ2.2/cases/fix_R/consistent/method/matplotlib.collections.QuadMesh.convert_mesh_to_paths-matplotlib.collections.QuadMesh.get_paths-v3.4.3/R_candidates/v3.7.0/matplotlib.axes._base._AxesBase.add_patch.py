    def add_patch(self, p):
        """
        Add a `.Patch` to the Axes; return the patch.
        """
        _api.check_isinstance(mpatches.Patch, p=p)
        self._set_artist_props(p)
        if p.get_clip_path() is None:
            p.set_clip_path(self.patch)
        self._update_patch_limits(p)
        self._children.append(p)
        p._remove_method = self._children.remove
        return p
