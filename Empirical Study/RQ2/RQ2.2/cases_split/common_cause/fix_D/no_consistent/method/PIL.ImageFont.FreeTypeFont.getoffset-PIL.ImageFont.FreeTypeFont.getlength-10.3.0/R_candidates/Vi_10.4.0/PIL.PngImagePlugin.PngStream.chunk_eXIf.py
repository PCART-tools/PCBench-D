    def chunk_eXIf(self, pos: int, length: int) -> bytes:
        s = ImageFile._safe_read(self.fp, length)
        self.im_info["exif"] = b"Exif\x00\x00" + s
        return s
