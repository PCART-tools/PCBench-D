    def _load_bitmaps(self, metrics):
        #
        # bitmap data

        bitmaps = []

        fp, format, i16, i32 = self._getformat(PCF_BITMAPS)

        nbitmaps = i32(fp.read(4))

        if nbitmaps != len(metrics):
            msg = "Wrong number of bitmaps"
            raise OSError(msg)

        offsets = []
        for i in range(nbitmaps):
            offsets.append(i32(fp.read(4)))

        bitmap_sizes = []
        for i in range(4):
            bitmap_sizes.append(i32(fp.read(4)))

        # byteorder = format & 4  # non-zero => MSB
        bitorder = format & 8  # non-zero => MSB
        padindex = format & 3

        bitmapsize = bitmap_sizes[padindex]
        offsets.append(bitmapsize)

        data = fp.read(bitmapsize)

        pad = BYTES_PER_ROW[padindex]
        mode = "1;R"
        if bitorder:
            mode = "1"

        for i in range(nbitmaps):
            xsize, ysize = metrics[i][:2]
            b, e = offsets[i : i + 2]
            bitmaps.append(
                Image.frombytes("1", (xsize, ysize), data[b:e], "raw", mode, pad(xsize))
            )

        return bitmaps
