    def set_clip_path(self, path):
        """Set the clip path to a `.TransformedPath` or None."""
        _api.check_isinstance((transforms.TransformedPath, None), path=path)
        self._clippath = path
