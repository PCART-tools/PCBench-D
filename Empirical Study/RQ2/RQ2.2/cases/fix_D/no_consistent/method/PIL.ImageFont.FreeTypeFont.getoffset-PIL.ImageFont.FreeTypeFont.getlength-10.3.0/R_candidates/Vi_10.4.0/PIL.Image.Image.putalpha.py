    def putalpha(self, alpha: Image | int) -> None:
        """
        Adds or replaces the alpha layer in this image.  If the image
        does not have an alpha layer, it's converted to "LA" or "RGBA".
        The new layer must be either "L" or "1".

        :param alpha: The new alpha layer.  This can either be an "L" or "1"
           image having the same size as this image, or an integer.
        """

        self._ensure_mutable()

        if self.mode not in ("LA", "PA", "RGBA"):
            # attempt to promote self to a matching alpha mode
            try:
                mode = getmodebase(self.mode) + "A"
                try:
                    self.im.setmode(mode)
                except (AttributeError, ValueError) as e:
                    # do things the hard way
                    im = self.im.convert(mode)
                    if im.mode not in ("LA", "PA", "RGBA"):
                        msg = "alpha channel could not be added"
                        raise ValueError(msg) from e  # sanity check
                    self.im = im
                self.pyaccess = None
                self._mode = self.im.mode
            except KeyError as e:
                msg = "illegal image mode"
                raise ValueError(msg) from e

        if self.mode in ("LA", "PA"):
            band = 1
        else:
            band = 3

        if isImageType(alpha):
            # alpha layer
            if alpha.mode not in ("1", "L"):
                msg = "illegal image mode"
                raise ValueError(msg)
            alpha.load()
            if alpha.mode == "1":
                alpha = alpha.convert("L")
        else:
            # constant alpha
            alpha = cast(int, alpha)  # see python/typing#1013
            try:
                self.im.fillband(band, alpha)
            except (AttributeError, ValueError):
                # do things the hard way
                alpha = new("L", self.size, alpha)
            else:
                return

        self.im.putband(alpha.im, band)
