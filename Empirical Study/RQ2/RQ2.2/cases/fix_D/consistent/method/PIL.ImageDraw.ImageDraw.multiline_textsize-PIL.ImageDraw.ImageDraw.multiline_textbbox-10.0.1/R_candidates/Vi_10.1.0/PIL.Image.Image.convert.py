    def convert(
        self, mode=None, matrix=None, dither=None, palette=Palette.WEB, colors=256
    ):
        """
        Returns a converted copy of this image. For the "P" mode, this
        method translates pixels through the palette.  If mode is
        omitted, a mode is chosen so that all information in the image
        and the palette can be represented without a palette.

        The current version supports all possible conversions between
        "L", "RGB" and "CMYK". The ``matrix`` argument only supports "L"
        and "RGB".

        When translating a color image to greyscale (mode "L"),
        the library uses the ITU-R 601-2 luma transform::

            L = R * 299/1000 + G * 587/1000 + B * 114/1000

        The default method of converting a greyscale ("L") or "RGB"
        image into a bilevel (mode "1") image uses Floyd-Steinberg
        dither to approximate the original image luminosity levels. If
        dither is ``None``, all values larger than 127 are set to 255 (white),
        all other values to 0 (black). To use other thresholds, use the
        :py:meth:`~PIL.Image.Image.point` method.

        When converting from "RGBA" to "P" without a ``matrix`` argument,
        this passes the operation to :py:meth:`~PIL.Image.Image.quantize`,
        and ``dither`` and ``palette`` are ignored.

        When converting from "PA", if an "RGBA" palette is present, the alpha
        channel from the image will be used instead of the values from the palette.

        :param mode: The requested mode. See: :ref:`concept-modes`.
        :param matrix: An optional conversion matrix.  If given, this
           should be 4- or 12-tuple containing floating point values.
        :param dither: Dithering method, used when converting from
           mode "RGB" to "P" or from "RGB" or "L" to "1".
           Available methods are :data:`Dither.NONE` or :data:`Dither.FLOYDSTEINBERG`
           (default). Note that this is not used when ``matrix`` is supplied.
        :param palette: Palette to use when converting from mode "RGB"
           to "P".  Available palettes are :data:`Palette.WEB` or
           :data:`Palette.ADAPTIVE`.
        :param colors: Number of colors to use for the :data:`Palette.ADAPTIVE`
           palette. Defaults to 256.
        :rtype: :py:class:`~PIL.Image.Image`
        :returns: An :py:class:`~PIL.Image.Image` object.
        """

        self.load()

        has_transparency = "transparency" in self.info
        if not mode and self.mode == "P":
            # determine default mode
            if self.palette:
                mode = self.palette.mode
            else:
                mode = "RGB"
            if mode == "RGB" and has_transparency:
                mode = "RGBA"
        if not mode or (mode == self.mode and not matrix):
            return self.copy()

        if matrix:
            # matrix conversion
            if mode not in ("L", "RGB"):
                msg = "illegal conversion"
                raise ValueError(msg)
            im = self.im.convert_matrix(mode, matrix)
            new_im = self._new(im)
            if has_transparency and self.im.bands == 3:
                transparency = new_im.info["transparency"]

                def convert_transparency(m, v):
                    v = m[0] * v[0] + m[1] * v[1] + m[2] * v[2] + m[3] * 0.5
                    return max(0, min(255, int(v)))

                if mode == "L":
                    transparency = convert_transparency(matrix, transparency)
                elif len(mode) == 3:
                    transparency = tuple(
                        convert_transparency(matrix[i * 4 : i * 4 + 4], transparency)
                        for i in range(0, len(transparency))
                    )
                new_im.info["transparency"] = transparency
            return new_im

        if mode == "P" and self.mode == "RGBA":
            return self.quantize(colors)

        trns = None
        delete_trns = False
        # transparency handling
        if has_transparency:
            if (self.mode in ("1", "L", "I") and mode in ("LA", "RGBA")) or (
                self.mode == "RGB" and mode == "RGBA"
            ):
                # Use transparent conversion to promote from transparent
                # color to an alpha channel.
                new_im = self._new(
                    self.im.convert_transparent(mode, self.info["transparency"])
                )
                del new_im.info["transparency"]
                return new_im
            elif self.mode in ("L", "RGB", "P") and mode in ("L", "RGB", "P"):
                t = self.info["transparency"]
                if isinstance(t, bytes):
                    # Dragons. This can't be represented by a single color
                    warnings.warn(
                        "Palette images with Transparency expressed in bytes should be "
                        "converted to RGBA images"
                    )
                    delete_trns = True
                else:
                    # get the new transparency color.
                    # use existing conversions
                    trns_im = new(self.mode, (1, 1))
                    if self.mode == "P":
                        trns_im.putpalette(self.palette)
                        if isinstance(t, tuple):
                            err = "Couldn't allocate a palette color for transparency"
                            try:
                                t = trns_im.palette.getcolor(t, self)
                            except ValueError as e:
                                if str(e) == "cannot allocate more than 256 colors":
                                    # If all 256 colors are in use,
                                    # then there is no need for transparency
                                    t = None
                                else:
                                    raise ValueError(err) from e
                    if t is None:
                        trns = None
                    else:
                        trns_im.putpixel((0, 0), t)

                        if mode in ("L", "RGB"):
                            trns_im = trns_im.convert(mode)
                        else:
                            # can't just retrieve the palette number, got to do it
                            # after quantization.
                            trns_im = trns_im.convert("RGB")
                        trns = trns_im.getpixel((0, 0))

            elif self.mode == "P" and mode in ("LA", "PA", "RGBA"):
                t = self.info["transparency"]
                delete_trns = True

                if isinstance(t, bytes):
                    self.im.putpalettealphas(t)
                elif isinstance(t, int):
                    self.im.putpalettealpha(t, 0)
                else:
                    msg = "Transparency for P mode should be bytes or int"
                    raise ValueError(msg)

        if mode == "P" and palette == Palette.ADAPTIVE:
            im = self.im.quantize(colors)
            new_im = self._new(im)
            from . import ImagePalette

            new_im.palette = ImagePalette.ImagePalette(
                "RGB", new_im.im.getpalette("RGB")
            )
            if delete_trns:
                # This could possibly happen if we requantize to fewer colors.
                # The transparency would be totally off in that case.
                del new_im.info["transparency"]
            if trns is not None:
                try:
                    new_im.info["transparency"] = new_im.palette.getcolor(trns, new_im)
                except Exception:
                    # if we can't make a transparent color, don't leave the old
                    # transparency hanging around to mess us up.
                    del new_im.info["transparency"]
                    warnings.warn("Couldn't allocate palette entry for transparency")
            return new_im

        if "LAB" in (self.mode, mode):
            other_mode = mode if self.mode == "LAB" else self.mode
            if other_mode in ("RGB", "RGBA", "RGBX"):
                from . import ImageCms

                srgb = ImageCms.createProfile("sRGB")
                lab = ImageCms.createProfile("LAB")
                profiles = [lab, srgb] if self.mode == "LAB" else [srgb, lab]
                transform = ImageCms.buildTransform(
                    profiles[0], profiles[1], self.mode, mode
                )
                return transform.apply(self)

        # colorspace conversion
        if dither is None:
            dither = Dither.FLOYDSTEINBERG

        try:
            im = self.im.convert(mode, dither)
        except ValueError:
            try:
                # normalize source image and try again
                modebase = getmodebase(self.mode)
                if modebase == self.mode:
                    raise
                im = self.im.convert(modebase)
                im = im.convert(mode, dither)
            except KeyError as e:
                msg = "illegal conversion"
                raise ValueError(msg) from e

        new_im = self._new(im)
        if mode == "P" and palette != Palette.ADAPTIVE:
            from . import ImagePalette

            new_im.palette = ImagePalette.ImagePalette("RGB", im.getpalette("RGB"))
        if delete_trns:
            # crash fail if we leave a bytes transparency in an rgb/l mode.
            del new_im.info["transparency"]
        if trns is not None:
            if new_im.mode == "P":
                try:
                    new_im.info["transparency"] = new_im.palette.getcolor(trns, new_im)
                except ValueError as e:
                    del new_im.info["transparency"]
                    if str(e) != "cannot allocate more than 256 colors":
                        # If all 256 colors are in use,
                        # then there is no need for transparency
                        warnings.warn(
                            "Couldn't allocate palette entry for transparency"
                        )
            else:
                new_im.info["transparency"] = trns
        return new_im
