    def set_clip_path(self, path, transform=None):
        """
        Set the artist's clip path, which may be:

        - a :class:`~matplotlib.patches.Patch` (or subclass) instance; or
        - a :class:`~matplotlib.path.Path` instance, in which case a
          :class:`~matplotlib.transforms.Transform` instance, which will be
          applied to the path before using it for clipping, must be provided;
          or
        - ``None``, to remove a previously set clipping path.

        For efficiency, if the path happens to be an axis-aligned rectangle,
        this method will set the clipping box to the corresponding rectangle
        and set the clipping path to ``None``.

        ACCEPTS: [ (:class:`~matplotlib.path.Path`,
        :class:`~matplotlib.transforms.Transform`) |
        :class:`~matplotlib.patches.Patch` | None ]
        """
        from matplotlib.patches import Patch, Rectangle

        success = False
        if transform is None:
            if isinstance(path, Rectangle):
                self.clipbox = TransformedBbox(Bbox.unit(),
                                               path.get_transform())
                self._clippath = None
                success = True
            elif isinstance(path, Patch):
                self._clippath = TransformedPatchPath(path)
                success = True
            elif isinstance(path, tuple):
                path, transform = path

        if path is None:
            self._clippath = None
            success = True
        elif isinstance(path, Path):
            self._clippath = TransformedPath(path, transform)
            success = True
        elif isinstance(path, TransformedPatchPath):
            self._clippath = path
            success = True
        elif isinstance(path, TransformedPath):
            self._clippath = path
            success = True

        if not success:
            raise TypeError(
                "Invalid arguments to set_clip_path, of type {} and {}"
                .format(type(path).__name__, type(transform).__name__))
        # This may result in the callbacks being hit twice, but guarantees they
        # will be hit at least once.
        self.pchanged()
        self.stale = True
