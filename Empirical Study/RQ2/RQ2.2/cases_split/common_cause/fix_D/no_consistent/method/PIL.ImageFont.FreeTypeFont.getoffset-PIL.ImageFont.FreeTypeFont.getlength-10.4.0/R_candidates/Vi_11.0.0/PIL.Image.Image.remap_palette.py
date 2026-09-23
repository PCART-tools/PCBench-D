    def remap_palette(
        self, dest_map: list[int], source_palette: bytes | bytearray | None = None
    ) -> Image:
        """
        Rewrites the image to reorder the palette.

        :param dest_map: A list of indexes into the original palette.
           e.g. ``[1,0]`` would swap a two item palette, and ``list(range(256))``
           is the identity transform.
        :param source_palette: Bytes or None.
        :returns:  An :py:class:`~PIL.Image.Image` object.

        """
        from . import ImagePalette

        if self.mode not in ("L", "P"):
            msg = "illegal image mode"
            raise ValueError(msg)

        bands = 3
        palette_mode = "RGB"
        if source_palette is None:
            if self.mode == "P":
                self.load()
                palette_mode = self.im.getpalettemode()
                if palette_mode == "RGBA":
                    bands = 4
                source_palette = self.im.getpalette(palette_mode, palette_mode)
            else:  # L-mode
                source_palette = bytearray(i // 3 for i in range(768))
        elif len(source_palette) > 768:
            bands = 4
            palette_mode = "RGBA"

        palette_bytes = b""
        new_positions = [0] * 256

        # pick only the used colors from the palette
        for i, oldPosition in enumerate(dest_map):
            palette_bytes += source_palette[
                oldPosition * bands : oldPosition * bands + bands
            ]
            new_positions[oldPosition] = i

        # replace the palette color id of all pixel with the new id

        # Palette images are [0..255], mapped through a 1 or 3
        # byte/color map.  We need to remap the whole image
        # from palette 1 to palette 2. New_positions is
        # an array of indexes into palette 1.  Palette 2 is
        # palette 1 with any holes removed.

        # We're going to leverage the convert mechanism to use the
        # C code to remap the image from palette 1 to palette 2,
        # by forcing the source image into 'L' mode and adding a
        # mapping 'L' mode palette, then converting back to 'L'
        # sans palette thus converting the image bytes, then
        # assigning the optimized RGB palette.

        # perf reference, 9500x4000 gif, w/~135 colors
        # 14 sec prepatch, 1 sec postpatch with optimization forced.

        mapping_palette = bytearray(new_positions)

        m_im = self.copy()
        m_im._mode = "P"

        m_im.palette = ImagePalette.ImagePalette(
            palette_mode, palette=mapping_palette * bands
        )
        # possibly set palette dirty, then
        # m_im.putpalette(mapping_palette, 'L')  # converts to 'P'
        # or just force it.
        # UNDONE -- this is part of the general issue with palettes
        m_im.im.putpalette(palette_mode, palette_mode + ";L", m_im.palette.tobytes())

        m_im = m_im.convert("L")

        m_im.putpalette(palette_bytes, palette_mode)
        m_im.palette = ImagePalette.ImagePalette(palette_mode, palette=palette_bytes)

        if "transparency" in self.info:
            try:
                m_im.info["transparency"] = dest_map.index(self.info["transparency"])
            except ValueError:
                if "transparency" in m_im.info:
                    del m_im.info["transparency"]

        return m_im
