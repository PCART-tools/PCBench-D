    def _load_properties(self) -> dict[bytes, bytes | int]:
        #
        # font properties

        properties = {}

        fp, format, i16, i32 = self._getformat(PCF_PROPERTIES)

        nprops = i32(fp.read(4))

        # read property description
        p = [(i32(fp.read(4)), i8(fp.read(1)), i32(fp.read(4))) for _ in range(nprops)]

        if nprops & 3:
            fp.seek(4 - (nprops & 3), io.SEEK_CUR)  # pad

        data = fp.read(i32(fp.read(4)))

        for k, s, v in p:
            property_value: bytes | int = sz(data, v) if s else v
            properties[sz(data, k)] = property_value

        return properties
