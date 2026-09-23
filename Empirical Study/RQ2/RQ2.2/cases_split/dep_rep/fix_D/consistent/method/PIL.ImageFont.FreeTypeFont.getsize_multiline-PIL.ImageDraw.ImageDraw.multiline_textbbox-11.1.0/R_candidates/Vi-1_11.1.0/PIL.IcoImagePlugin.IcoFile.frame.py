    def frame(self, idx: int) -> Image.Image:
        """
        Get an image from frame idx
        """

        header = self.entry[idx]

        self.buf.seek(header.offset)
        data = self.buf.read(8)
        self.buf.seek(header.offset)

        im: Image.Image
        if data[:8] == PngImagePlugin._MAGIC:
            # png frame
            im = PngImagePlugin.PngImageFile(self.buf)
            Image._decompression_bomb_check(im.size)
        else:
            # XOR + AND mask bmp frame
            im = BmpImagePlugin.DibImageFile(self.buf)
            Image._decompression_bomb_check(im.size)

            # change tile dimension to only encompass XOR image
            im._size = (im.size[0], int(im.size[1] / 2))
            d, e, o, a = im.tile[0]
            im.tile[0] = ImageFile._Tile(d, (0, 0) + im.size, o, a)

            # figure out where AND mask image starts
            if header.bpp == 32:
                # 32-bit color depth icon image allows semitransparent areas
                # PIL's DIB format ignores transparency bits, recover them.
                # The DIB is packed in BGRX byte order where X is the alpha
                # channel.

                # Back up to start of bmp data
                self.buf.seek(o)
                # extract every 4th byte (eg. 3,7,11,15,...)
                alpha_bytes = self.buf.read(im.size[0] * im.size[1] * 4)[3::4]

                # convert to an 8bpp grayscale image
                try:
                    mask = Image.frombuffer(
                        "L",  # 8bpp
                        im.size,  # (w, h)
                        alpha_bytes,  # source chars
                        "raw",  # raw decoder
                        ("L", 0, -1),  # 8bpp inverted, unpadded, reversed
                    )
                except ValueError:
                    if ImageFile.LOAD_TRUNCATED_IMAGES:
                        mask = None
                    else:
                        raise
            else:
                # get AND image from end of bitmap
                w = im.size[0]
                if (w % 32) > 0:
                    # bitmap row data is aligned to word boundaries
                    w += 32 - (im.size[0] % 32)

                # the total mask data is
                # padded row size * height / bits per char

                total_bytes = int((w * im.size[1]) / 8)
                and_mask_offset = header.offset + header.size - total_bytes

                self.buf.seek(and_mask_offset)
                mask_data = self.buf.read(total_bytes)

                # convert raw data to image
                try:
                    mask = Image.frombuffer(
                        "1",  # 1 bpp
                        im.size,  # (w, h)
                        mask_data,  # source chars
                        "raw",  # raw decoder
                        ("1;I", int(w / 8), -1),  # 1bpp inverted, padded, reversed
                    )
                except ValueError:
                    if ImageFile.LOAD_TRUNCATED_IMAGES:
                        mask = None
                    else:
                        raise

                # now we have two images, im is XOR image and mask is AND image

            # apply mask image as alpha channel
            if mask:
                im = im.convert("RGBA")
                im.putalpha(mask)

        return im
