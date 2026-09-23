    def _writePng(self, img):
        """
        Write the image *img* into the pdf file using png
        predictors with Flate compression.
        """
        buffer = BytesIO()
        img.save(buffer, format="png")
        buffer.seek(8)
        png_data = b''
        bit_depth = palette = None
        while True:
            length, type = struct.unpack(b'!L4s', buffer.read(8))
            if type in [b'IHDR', b'PLTE', b'IDAT']:
                data = buffer.read(length)
                if len(data) != length:
                    raise RuntimeError("truncated data")
                if type == b'IHDR':
                    bit_depth = int(data[8])
                elif type == b'PLTE':
                    palette = data
                elif type == b'IDAT':
                    png_data += data
            elif type == b'IEND':
                break
            else:
                buffer.seek(length, 1)
            buffer.seek(4, 1)   # skip CRC
        return png_data, bit_depth, palette
