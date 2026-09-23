    def transform(
        self,
        size,
        method,
        data=None,
        resample=Resampling.NEAREST,
        fill=1,
        fillcolor=None,
    ) -> Image:
        """
        Transforms this image.  This method creates a new image with the
        given size, and the same mode as the original, and copies data
        to the new image using the given transform.

        :param size: The output size in pixels, as a 2-tuple:
           (width, height).
        :param method: The transformation method.  This is one of
          :py:data:`Transform.EXTENT` (cut out a rectangular subregion),
          :py:data:`Transform.AFFINE` (affine transform),
          :py:data:`Transform.PERSPECTIVE` (perspective transform),
          :py:data:`Transform.QUAD` (map a quadrilateral to a rectangle), or
          :py:data:`Transform.MESH` (map a number of source quadrilaterals
          in one operation).

          It may also be an :py:class:`~PIL.Image.ImageTransformHandler`
          object::

            class Example(Image.ImageTransformHandler):
                def transform(self, size, data, resample, fill=1):
                    # Return result

          Implementations of :py:class:`~PIL.Image.ImageTransformHandler`
          for some of the :py:class:`Transform` methods are provided
          in :py:mod:`~PIL.ImageTransform`.

          It may also be an object with a ``method.getdata`` method
          that returns a tuple supplying new ``method`` and ``data`` values::

            class Example:
                def getdata(self):
                    method = Image.Transform.EXTENT
                    data = (0, 0, 100, 100)
                    return method, data
        :param data: Extra data to the transformation method.
        :param resample: Optional resampling filter.  It can be one of
           :py:data:`Resampling.NEAREST` (use nearest neighbour),
           :py:data:`Resampling.BILINEAR` (linear interpolation in a 2x2
           environment), or :py:data:`Resampling.BICUBIC` (cubic spline
           interpolation in a 4x4 environment). If omitted, or if the image
           has mode "1" or "P", it is set to :py:data:`Resampling.NEAREST`.
           See: :ref:`concept-filters`.
        :param fill: If ``method`` is an
          :py:class:`~PIL.Image.ImageTransformHandler` object, this is one of
          the arguments passed to it. Otherwise, it is unused.
        :param fillcolor: Optional fill color for the area outside the
           transform in the output image.
        :returns: An :py:class:`~PIL.Image.Image` object.
        """

        if self.mode in ("LA", "RGBA") and resample != Resampling.NEAREST:
            return (
                self.convert({"LA": "La", "RGBA": "RGBa"}[self.mode])
                .transform(size, method, data, resample, fill, fillcolor)
                .convert(self.mode)
            )

        if isinstance(method, ImageTransformHandler):
            return method.transform(size, self, resample=resample, fill=fill)

        if hasattr(method, "getdata"):
            # compatibility w. old-style transform objects
            method, data = method.getdata()

        if data is None:
            msg = "missing method data"
            raise ValueError(msg)

        im = new(self.mode, size, fillcolor)
        if self.mode == "P" and self.palette:
            im.palette = self.palette.copy()
        im.info = self.info.copy()
        if method == Transform.MESH:
            # list of quads
            for box, quad in data:
                im.__transformer(
                    box, self, Transform.QUAD, quad, resample, fillcolor is None
                )
        else:
            im.__transformer(
                (0, 0) + size, self, method, data, resample, fillcolor is None
            )

        return im
