    def _load_metrics(self):
        #
        # font metrics

        metrics = []

        fp, format, i16, i32 = self._getformat(PCF_METRICS)

        append = metrics.append

        if (format & 0xFF00) == 0x100:
            # "compressed" metrics
            for i in range(i16(fp.read(2))):
                left = i8(fp.read(1)) - 128
                right = i8(fp.read(1)) - 128
                width = i8(fp.read(1)) - 128
                ascent = i8(fp.read(1)) - 128
                descent = i8(fp.read(1)) - 128
                xsize = right - left
                ysize = ascent + descent
                append((xsize, ysize, left, right, width, ascent, descent, 0))

        else:
            # "jumbo" metrics
            for i in range(i32(fp.read(4))):
                left = i16(fp.read(2))
                right = i16(fp.read(2))
                width = i16(fp.read(2))
                ascent = i16(fp.read(2))
                descent = i16(fp.read(2))
                attributes = i16(fp.read(2))
                xsize = right - left
                ysize = ascent + descent
                append((xsize, ysize, left, right, width, ascent, descent, attributes))

        return metrics
