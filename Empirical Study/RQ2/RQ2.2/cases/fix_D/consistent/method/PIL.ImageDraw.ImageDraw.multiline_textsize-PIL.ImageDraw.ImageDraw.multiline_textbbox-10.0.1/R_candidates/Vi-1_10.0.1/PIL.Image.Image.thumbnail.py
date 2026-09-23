    def thumbnail(self, size, resample=Resampling.BICUBIC, reducing_gap=2.0):
        """
        Make this image into a thumbnail.  This method modifies the
        image to contain a thumbnail version of itself, no larger than
        the given size.  This method calculates an appropriate thumbnail
        size to preserve the aspect of the image, calls the
        :py:meth:`~PIL.Image.Image.draft` method to configure the file reader
        (where applicable), and finally resizes the image.

        Note that this function modifies the :py:class:`~PIL.Image.Image`
        object in place.  If you need to use the full resolution image as well,
        apply this method to a :py:meth:`~PIL.Image.Image.copy` of the original
        image.

        :param size: The requested size in pixels, as a 2-tuple:
           (width, height).
        :param resample: Optional resampling filter.  This can be one
           of :py:data:`Resampling.NEAREST`, :py:data:`Resampling.BOX`,
           :py:data:`Resampling.BILINEAR`, :py:data:`Resampling.HAMMING`,
           :py:data:`Resampling.BICUBIC` or :py:data:`Resampling.LANCZOS`.
           If omitted, it defaults to :py:data:`Resampling.BICUBIC`.
           (was :py:data:`Resampling.NEAREST` prior to version 2.5.0).
           See: :ref:`concept-filters`.
        :param reducing_gap: Apply optimization by resizing the image
           in two steps. First, reducing the image by integer times
           using :py:meth:`~PIL.Image.Image.reduce` or
           :py:meth:`~PIL.Image.Image.draft` for JPEG images.
           Second, resizing using regular resampling. The last step
           changes size no less than by ``reducing_gap`` times.
           ``reducing_gap`` may be None (no first step is performed)
           or should be greater than 1.0. The bigger ``reducing_gap``,
           the closer the result to the fair resampling.
           The smaller ``reducing_gap``, the faster resizing.
           With ``reducing_gap`` greater or equal to 3.0, the result is
           indistinguishable from fair resampling in most cases.
           The default value is 2.0 (very close to fair resampling
           while still being faster in many cases).
        :returns: None
        """

        provided_size = tuple(map(math.floor, size))

        def preserve_aspect_ratio():
            def round_aspect(number, key):
                return max(min(math.floor(number), math.ceil(number), key=key), 1)

            x, y = provided_size
            if x >= self.width and y >= self.height:
                return

            aspect = self.width / self.height
            if x / y >= aspect:
                x = round_aspect(y * aspect, key=lambda n: abs(aspect - n / y))
            else:
                y = round_aspect(
                    x / aspect, key=lambda n: 0 if n == 0 else abs(aspect - x / n)
                )
            return x, y

        box = None
        if reducing_gap is not None:
            size = preserve_aspect_ratio()
            if size is None:
                return

            res = self.draft(None, (size[0] * reducing_gap, size[1] * reducing_gap))
            if res is not None:
                box = res[1]
        if box is None:
            self.load()

            # load() may have changed the size of the image
            size = preserve_aspect_ratio()
            if size is None:
                return

        if self.size != size:
            im = self.resize(size, resample, box=box, reducing_gap=reducing_gap)

            self.im = im.im
            self._size = size
            self.mode = self.im.mode

        self.readonly = 0
        self.pyaccess = None
