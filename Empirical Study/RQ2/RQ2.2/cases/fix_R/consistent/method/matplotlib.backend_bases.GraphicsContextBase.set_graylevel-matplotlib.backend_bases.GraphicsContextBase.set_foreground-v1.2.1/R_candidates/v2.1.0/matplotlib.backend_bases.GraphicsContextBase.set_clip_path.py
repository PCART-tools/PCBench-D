    def set_clip_path(self, path):
        """
        Set the clip path and transformation.  Path should be a
        :class:`~matplotlib.transforms.TransformedPath` instance.
        """
        if path is not None and not isinstance(path,
                transforms.TransformedPath):
            msg = ("Path should be a matplotlib.transforms.TransformedPath"
                   "instance.")
            raise ValueError(msg)
        self._clippath = path
