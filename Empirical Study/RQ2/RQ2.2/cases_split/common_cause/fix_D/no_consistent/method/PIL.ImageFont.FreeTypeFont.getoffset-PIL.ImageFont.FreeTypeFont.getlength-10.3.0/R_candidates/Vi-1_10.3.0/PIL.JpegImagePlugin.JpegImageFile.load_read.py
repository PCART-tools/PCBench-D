    def load_read(self, read_bytes):
        """
        internal: read more image data
        For premature EOF and LOAD_TRUNCATED_IMAGES adds EOI marker
        so libjpeg can finish decoding
        """
        s = self.fp.read(read_bytes)

        if not s and ImageFile.LOAD_TRUNCATED_IMAGES and not hasattr(self, "_ended"):
            # Premature EOF.
            # Pretend file is finished adding EOI marker
            self._ended = True
            return b"\xFF\xD9"

        return s
