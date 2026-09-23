    def _open(self) -> None:
        if not SUPPORTED:
            msg = "image file could not be opened because AVIF support not installed"
            raise SyntaxError(msg)

        if DECODE_CODEC_CHOICE != "auto" and not _avif.decoder_codec_available(
            DECODE_CODEC_CHOICE
        ):
            msg = "Invalid opening codec"
            raise ValueError(msg)
        self._decoder = _avif.AvifDecoder(
            self.fp.read(),
            DECODE_CODEC_CHOICE,
            _get_default_max_threads(),
        )

        # Get info from decoder
        self._size, self.n_frames, self._mode, icc, exif, exif_orientation, xmp = (
            self._decoder.get_info()
        )
        self.is_animated = self.n_frames > 1

        if icc:
            self.info["icc_profile"] = icc
        if xmp:
            self.info["xmp"] = xmp

        if exif_orientation != 1 or exif:
            exif_data = Image.Exif()
            if exif:
                exif_data.load(exif)
                original_orientation = exif_data.get(ExifTags.Base.Orientation, 1)
            else:
                original_orientation = 1
            if exif_orientation != original_orientation:
                exif_data[ExifTags.Base.Orientation] = exif_orientation
                exif = exif_data.tobytes()
        if exif:
            self.info["exif"] = exif
        self.seek(0)
