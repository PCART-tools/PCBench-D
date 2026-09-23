    def set_clip_path(self, path, transform=None):
        """
        Set the artist's clip path.

        Parameters
        ----------
        path : `.Patch` or `.Path` or `.TransformedPath` or None
            The clip path. If given a `.Path`, *transform* must be provided as
            well. If *None*, a previously set clip path is removed.
        transform : `~matplotlib.transforms.Transform`, optional
            Only used if *path* is a `.Path`, in which case the given `.Path`
            is converted to a `.TransformedPath` using *transform*.

        Notes
        -----
        For efficiency, if *path* is a `.Rectangle` this method will set the
        clipping box to the corresponding rectangle and set the clipping path
        to ``None``.

        For technical reasons (support of ``setp``), a tuple
        (*path*, *transform*) is also accepted as a single positional
        parameter.

        .. ACCEPTS: Patch or (Path, Transform) or None
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
