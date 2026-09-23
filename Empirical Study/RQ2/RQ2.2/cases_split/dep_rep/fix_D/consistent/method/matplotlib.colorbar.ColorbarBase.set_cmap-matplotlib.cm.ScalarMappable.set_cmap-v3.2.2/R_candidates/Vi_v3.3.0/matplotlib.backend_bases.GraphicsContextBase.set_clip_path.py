    def set_clip_path(self, path):
        """
        Set the clip path and transformation.

        Parameters
        ----------
        path : `~matplotlib.transforms.TransformedPath` or None
        """
        cbook._check_isinstance((transforms.TransformedPath, None), path=path)
        self._clippath = path
