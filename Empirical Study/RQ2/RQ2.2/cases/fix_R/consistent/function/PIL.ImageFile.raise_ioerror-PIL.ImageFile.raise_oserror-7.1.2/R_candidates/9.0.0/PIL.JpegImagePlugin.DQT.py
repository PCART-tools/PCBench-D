def DQT(self, marker):
    #
    # Define quantization table.  Note that there might be more
    # than one table in each marker.

    # FIXME: The quantization tables can be used to estimate the
    # compression quality.

    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    while len(s):
        v = s[0]
        precision = 1 if (v // 16 == 0) else 2  # in bytes
        qt_length = 1 + precision * 64
        if len(s) < qt_length:
            raise SyntaxError("bad quantization table marker")
        data = array.array("B" if precision == 1 else "H", s[1:qt_length])
        if sys.byteorder == "little" and precision > 1:
            data.byteswap()  # the values are always big-endian
        self.quantization[v & 15] = [data[i] for i in zigzag_index]
        s = s[qt_length:]
