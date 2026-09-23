    def resize(self, size, resample=None, box=None, reducing_gap=None) -> Image:
        """
        Returns a resized copy of this image.

        :param size: The requested size in pixels, as a 2-tuple:
           (width, height).
        :param resample: An optional resampling filter.  This can be
           one of :py:data:`Resampling.NEAREST`, :py:data:`Resampling.BOX`,
           :py:data:`Resampling.BILINEAR`, :py:data:`Resampling.HAMMING`,
           :py:data:`Resampling.BICUBIC` or :py:data:`Resampling.LANCZOS`.
           If the image has mode "1" or "P", it is always set to
           :py:data:`Resampling.NEAREST`. If the image mode specifies a number
           of bits, such as "I;16", then the default filter is
           :py:data:`Resampling.NEAREST`. Otherwise, the default filter is
           :py:data:`Resampling.BICUBIC`. See: :ref:`concept-filters`.
        :param box: An optional 4-tuple of floats providing
           the source image region to be scaled.
           The values must be within (0, 0, width, height) rectangle.
           If omitted or None, the entire source is used.
        :param reducing_gap: Apply optimization by resizing the image
           in two steps. First, reducing the image by integer times
           using :py:meth:`~PIL.Image.Image.reduce`.
           Second, resizing using regular resampling. The last step
           changes size no less than by ``reducing_gap`` times.
           ``reducing_gap`` may be None (no first step is performed)
           or should be greater than 1.0. The bigger ``reducing_gap``,
           the closer the result to the fair resampling.
           The smaller ``reducing_gap``, the faster resizing.
           With ``reducing_gap`` greater or equal to 3.0, the result is
           indistinguishable from fair resampling in most cases.
           The default value is None (no optimization).
        :returns: An :py:class:`~PIL.Image.Image` object.
        """

        if resample is None:
            type_special = ";" in self.mode
            resample = Resampling.NEAREST if type_special else Resampling.BICUBIC
        elif resample not in (
            Resampling.NEAREST,
            Resampling.BILINEAR,
            Resampling.BICUBIC,
            Resampling.LANCZOS,
            Resampling.BOX,
            Resampling.HAMMING,
        ):
            msg = f"Unknown resampling filter ({resample})."

            filters = [
                f"{filter[1]} ({filter[0]})"
                for filter in (
                    (Resampling.NEAREST, "Image.Resampling.NEAREST"),
                    (Resampling.LANCZOS, "Image.Resampling.LANCZOS"),
                    (Resampling.BILINEAR, "Image.Resampling.BILINEAR"),
                    (Resampling.BICUBIC, "Image.Resampling.BICUBIC"),
                    (Resampling.BOX, "Image.Resampling.BOX"),
                    (Resampling.HAMMING, "Image.Resampling.HAMMING"),
                )
            ]
            msg += " Use " + ", ".join(filters[:-1]) + " or " + filters[-1]
            raise ValueError(msg)

        if reducing_gap is not None and reducing_gap < 1.0:
            msg = "reducing_gap must be 1.0 or greater"
            raise ValueError(msg)

        size = tuple(size)

        self.load()
        if box is None:
            box = (0, 0) + self.size
        else:
            box = tuple(box)

        if self.size == size and box == (0, 0) + self.size:
            return self.copy()

        if self.mode in ("1", "P"):
            resample = Resampling.NEAREST

        if self.mode in ["LA", "RGBA"] and resample != Resampling.NEAREST:
            im = self.convert({"LA": "La", "RGBA": "RGBa"}[self.mode])
            im = im.resize(size, resample, box)
            return im.convert(self.mode)

        self.load()

        if reducing_gap is not None and resample != Resampling.NEAREST:
            factor_x = int((box[2] - box[0]) / size[0] / reducing_gap) or 1
            factor_y = int((box[3] - box[1]) / size[1] / reducing_gap) or 1
            if factor_x > 1 or factor_y > 1:
                reduce_box = self._get_safe_box(size, resample, box)
                factor = (factor_x, factor_y)
                self = (
                    self.reduce(factor, box=reduce_box)
                    if callable(self.reduce)
                    else Image.reduce(self, factor, box=reduce_box)
                )
                box = (
                    (box[0] - reduce_box[0]) / factor_x,
                    (box[1] - reduce_box[1]) / factor_y,
                    (box[2] - reduce_box[0]) / factor_x,
                    (box[3] - reduce_box[1]) / factor_y,
                )

        return self._new(self.im.resize(size, resample, box))
