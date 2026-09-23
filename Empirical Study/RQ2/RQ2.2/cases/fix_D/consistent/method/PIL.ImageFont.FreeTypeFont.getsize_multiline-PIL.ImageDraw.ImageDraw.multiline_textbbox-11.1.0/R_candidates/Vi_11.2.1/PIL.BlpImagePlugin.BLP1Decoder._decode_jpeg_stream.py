    def _decode_jpeg_stream(self) -> None:
        from .JpegImagePlugin import JpegImageFile

        (jpeg_header_size,) = struct.unpack("<I", self._safe_read(4))
        jpeg_header = self._safe_read(jpeg_header_size)
        assert self.fd is not None
        self._safe_read(self._offsets[0] - self.fd.tell())  # What IS this?
        data = self._safe_read(self._lengths[0])
        data = jpeg_header + data
        image = JpegImageFile(BytesIO(data))
        Image._decompression_bomb_check(image.size)
        if image.mode == "CMYK":
            args = image.tile[0].args
            assert isinstance(args, tuple)
            image.tile = [image.tile[0]._replace(args=(args[0], "CMYK"))]
        self.set_as_raw(image.convert("RGB").tobytes(), "BGR")
