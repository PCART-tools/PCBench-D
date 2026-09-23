    def _writePng(self, data):
        """
        Write the image *data* into the pdf file using png
        predictors with Flate compression.
        """
        buffer = BytesIO()
        if data.shape[-1] == 1:
            data = data.squeeze(axis=-1)
        Image.fromarray(data).save(buffer, format="png")
        buffer.seek(8)
        while True:
            length, type = struct.unpack(b'!L4s', buffer.read(8))
            if type == b'IDAT':
                data = buffer.read(length)
                if len(data) != length:
                    raise RuntimeError("truncated data")
                self.currentstream.write(data)
            elif type == b'IEND':
                break
            else:
                buffer.seek(length, 1)
            buffer.seek(4, 1)   # skip CRC
