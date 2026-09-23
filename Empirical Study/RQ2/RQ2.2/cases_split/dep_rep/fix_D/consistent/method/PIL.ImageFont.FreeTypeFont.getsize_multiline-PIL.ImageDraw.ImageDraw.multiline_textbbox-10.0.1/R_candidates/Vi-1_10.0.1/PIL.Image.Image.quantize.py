    def quantize(
        self,
        colors=256,
        method=None,
        kmeans=0,
        palette=None,
        dither=Dither.FLOYDSTEINBERG,
    ):
        """
        Convert the image to 'P' mode with the specified number
        of colors.

        :param colors: The desired number of colors, <= 256
        :param method: :data:`Quantize.MEDIANCUT` (median cut),
                       :data:`Quantize.MAXCOVERAGE` (maximum coverage),
                       :data:`Quantize.FASTOCTREE` (fast octree),
                       :data:`Quantize.LIBIMAGEQUANT` (libimagequant; check support
                       using :py:func:`PIL.features.check_feature` with
                       ``feature="libimagequant"``).

                       By default, :data:`Quantize.MEDIANCUT` will be used.

                       The exception to this is RGBA images. :data:`Quantize.MEDIANCUT`
                       and :data:`Quantize.MAXCOVERAGE` do not support RGBA images, so
                       :data:`Quantize.FASTOCTREE` is used by default instead.
        :param kmeans: Integer
        :param palette: Quantize to the palette of given
                        :py:class:`PIL.Image.Image`.
        :param dither: Dithering method, used when converting from
           mode "RGB" to "P" or from "RGB" or "L" to "1".
           Available methods are :data:`Dither.NONE` or :data:`Dither.FLOYDSTEINBERG`
           (default).
        :returns: A new image
        """

        self.load()

        if method is None:
            # defaults:
            method = Quantize.MEDIANCUT
            if self.mode == "RGBA":
                method = Quantize.FASTOCTREE

        if self.mode == "RGBA" and method not in (
            Quantize.FASTOCTREE,
            Quantize.LIBIMAGEQUANT,
        ):
            # Caller specified an invalid mode.
            msg = (
                "Fast Octree (method == 2) and libimagequant (method == 3) "
                "are the only valid methods for quantizing RGBA images"
            )
            raise ValueError(msg)

        if palette:
            # use palette from reference image
            palette.load()
            if palette.mode != "P":
                msg = "bad mode for palette image"
                raise ValueError(msg)
            if self.mode != "RGB" and self.mode != "L":
                msg = "only RGB or L mode images can be quantized to a palette"
                raise ValueError(msg)
            im = self.im.convert("P", dither, palette.im)
            new_im = self._new(im)
            new_im.palette = palette.palette.copy()
            return new_im

        im = self._new(self.im.quantize(colors, method, kmeans))

        from . import ImagePalette

        mode = im.im.getpalettemode()
        palette = im.im.getpalette(mode, mode)[: colors * len(mode)]
        im.palette = ImagePalette.ImagePalette(mode, palette)

        return im
