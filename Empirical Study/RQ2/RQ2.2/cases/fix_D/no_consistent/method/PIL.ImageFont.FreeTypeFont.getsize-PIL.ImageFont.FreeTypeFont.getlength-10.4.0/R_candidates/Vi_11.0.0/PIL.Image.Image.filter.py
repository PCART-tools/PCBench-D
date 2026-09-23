    def filter(self, filter: ImageFilter.Filter | type[ImageFilter.Filter]) -> Image:
        """
        Filters this image using the given filter.  For a list of
        available filters, see the :py:mod:`~PIL.ImageFilter` module.

        :param filter: Filter kernel.
        :returns: An :py:class:`~PIL.Image.Image` object."""

        from . import ImageFilter

        self.load()

        if callable(filter):
            filter = filter()
        if not hasattr(filter, "filter"):
            msg = "filter argument should be ImageFilter.Filter instance or class"
            raise TypeError(msg)

        multiband = isinstance(filter, ImageFilter.MultibandFilter)
        if self.im.bands == 1 or multiband:
            return self._new(filter.filter(self.im))

        ims = [
            self._new(filter.filter(self.im.getband(c))) for c in range(self.im.bands)
        ]
        return merge(self.mode, ims)
