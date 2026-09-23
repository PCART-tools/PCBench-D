    def _writePng(self, data):
        """
        Write the image *data* into the pdf file using png
        predictors with Flate compression.
        """

        buffer = BytesIO()
        _png.write_png(data, buffer)
        buffer.seek(8)
        written = 0
        header = bytearray(8)
        while True:
            n = buffer.readinto(header)
            assert n == 8
            length, type = struct.unpack(b'!L4s', bytes(header))
            if type == b'IDAT':
                data = bytearray(length)
                n = buffer.readinto(data)
                assert n == length
                self.currentstream.write(bytes(data))
                written += n
            elif type == b'IEND':
                break
            else:
                buffer.seek(length, 1)
            buffer.seek(4, 1)   # skip CRC
