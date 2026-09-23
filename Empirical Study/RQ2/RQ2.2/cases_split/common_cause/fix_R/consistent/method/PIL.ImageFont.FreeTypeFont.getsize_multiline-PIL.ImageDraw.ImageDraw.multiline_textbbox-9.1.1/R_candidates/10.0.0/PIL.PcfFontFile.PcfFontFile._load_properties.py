    def _load_properties(self):
        #
        # font properties

        properties = {}

        fp, format, i16, i32 = self._getformat(PCF_PROPERTIES)

        nprops = i32(fp.read(4))

        # read property description
        p = []
        for i in range(nprops):
            p.append((i32(fp.read(4)), i8(fp.read(1)), i32(fp.read(4))))
        if nprops & 3:
            fp.seek(4 - (nprops & 3), io.SEEK_CUR)  # pad

        data = fp.read(i32(fp.read(4)))

        for k, s, v in p:
            k = sz(data, k)
            if s:
                v = sz(data, v)
            properties[k] = v

        return properties
