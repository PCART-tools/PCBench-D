    @classmethod
    def interpret_trailer(cls, trailer_data: bytes) -> dict[bytes, Any]:
        trailer = {}
        offset = 0
        while True:
            m = cls.re_name.match(trailer_data, offset)
            if not m:
                m = cls.re_dict_end.match(trailer_data, offset)
                check_format_condition(
                    m is not None and m.end() == len(trailer_data),
                    "name not found in trailer, remaining data: "
                    + repr(trailer_data[offset:]),
                )
                break
            key = cls.interpret_name(m.group(1))
            assert isinstance(key, bytes)
            value, value_offset = cls.get_value(trailer_data, m.end())
            trailer[key] = value
            if value_offset is None:
                break
            offset = value_offset
        check_format_condition(
            b"Size" in trailer and isinstance(trailer[b"Size"], int),
            "/Size not in trailer or not an integer",
        )
        check_format_condition(
            b"Root" in trailer and isinstance(trailer[b"Root"], IndirectReference),
            "/Root not in trailer or not an indirect reference",
        )
        return trailer
