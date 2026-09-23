    def _open(self) -> None:
        if not _webp.HAVE_WEBPANIM:
            # Legacy mode
            data, width, height, self._mode, icc_profile, exif = _webp.WebPDecode(
                self.fp.read()
            )
            if icc_profile:
                self.info["icc_profile"] = icc_profile
            if exif:
                self.info["exif"] = exif
            self._size = width, height
            self.fp = BytesIO(data)
            self.tile = [("raw", (0, 0) + self.size, 0, self.mode)]
            self.n_frames = 1
            self.is_animated = False
            return

        # Use the newer AnimDecoder API to parse the (possibly) animated file,
        # and access muxed chunks like ICC/EXIF/XMP.
        self._decoder = _webp.WebPAnimDecoder(self.fp.read())

        # Get info from decoder
        width, height, loop_count, bgcolor, frame_count, mode = self._decoder.get_info()
        self._size = width, height
        self.info["loop"] = loop_count
        bg_a, bg_r, bg_g, bg_b = (
            (bgcolor >> 24) & 0xFF,
            (bgcolor >> 16) & 0xFF,
            (bgcolor >> 8) & 0xFF,
            bgcolor & 0xFF,
        )
        self.info["background"] = (bg_r, bg_g, bg_b, bg_a)
        self.n_frames = frame_count
        self.is_animated = self.n_frames > 1
        self._mode = "RGB" if mode == "RGBX" else mode
        self.rawmode = mode
        self.tile = []

        # Attempt to read ICC / EXIF / XMP chunks from file
        icc_profile = self._decoder.get_chunk("ICCP")
        exif = self._decoder.get_chunk("EXIF")
        xmp = self._decoder.get_chunk("XMP ")
        if icc_profile:
            self.info["icc_profile"] = icc_profile
        if exif:
            self.info["exif"] = exif
        if xmp:
            self.info["xmp"] = xmp

        # Initialize seek state
        self._reset(reset=False)
