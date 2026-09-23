    @classmethod
    def get_value(
        cls,
        data: bytes | bytearray | mmap.mmap,
        offset: int,
        expect_indirect: IndirectReference | None = None,
        max_nesting: int = -1,
    ) -> tuple[Any, int | None]:
        if max_nesting == 0:
            return None, None
        m = cls.re_comment.match(data, offset)
        if m:
            offset = m.end()
        m = cls.re_indirect_def_start.match(data, offset)
        if m:
            check_format_condition(
                int(m.group(1)) > 0,
                "indirect object definition: object ID must be greater than 0",
            )
            check_format_condition(
                int(m.group(2)) >= 0,
                "indirect object definition: generation must be non-negative",
            )
            check_format_condition(
                expect_indirect is None
                or expect_indirect
                == IndirectReference(int(m.group(1)), int(m.group(2))),
                "indirect object definition different than expected",
            )
            object, object_offset = cls.get_value(
                data, m.end(), max_nesting=max_nesting - 1
            )
            if object_offset is None:
                return object, None
            m = cls.re_indirect_def_end.match(data, object_offset)
            check_format_condition(
                m is not None, "indirect object definition end not found"
            )
            assert m is not None
            return object, m.end()
        check_format_condition(
            not expect_indirect, "indirect object definition not found"
        )
        m = cls.re_indirect_reference.match(data, offset)
        if m:
            check_format_condition(
                int(m.group(1)) > 0,
                "indirect object reference: object ID must be greater than 0",
            )
            check_format_condition(
                int(m.group(2)) >= 0,
                "indirect object reference: generation must be non-negative",
            )
            return IndirectReference(int(m.group(1)), int(m.group(2))), m.end()
        m = cls.re_dict_start.match(data, offset)
        if m:
            offset = m.end()
            result: dict[Any, Any] = {}
            m = cls.re_dict_end.match(data, offset)
            current_offset: int | None = offset
            while not m:
                assert current_offset is not None
                key, current_offset = cls.get_value(
                    data, current_offset, max_nesting=max_nesting - 1
                )
                if current_offset is None:
                    return result, None
                value, current_offset = cls.get_value(
                    data, current_offset, max_nesting=max_nesting - 1
                )
                result[key] = value
                if current_offset is None:
                    return result, None
                m = cls.re_dict_end.match(data, current_offset)
            current_offset = m.end()
            m = cls.re_stream_start.match(data, current_offset)
            if m:
                stream_len = result.get(b"Length")
                if stream_len is None or not isinstance(stream_len, int):
                    msg = f"bad or missing Length in stream dict ({stream_len})"
                    raise PdfFormatError(msg)
                stream_data = data[m.end() : m.end() + stream_len]
                m = cls.re_stream_end.match(data, m.end() + stream_len)
                check_format_condition(m is not None, "stream end not found")
                assert m is not None
                current_offset = m.end()
                return PdfStream(PdfDict(result), stream_data), current_offset
            return PdfDict(result), current_offset
        m = cls.re_array_start.match(data, offset)
        if m:
            offset = m.end()
            results = []
            m = cls.re_array_end.match(data, offset)
            current_offset = offset
            while not m:
                assert current_offset is not None
                value, current_offset = cls.get_value(
                    data, current_offset, max_nesting=max_nesting - 1
                )
                results.append(value)
                if current_offset is None:
                    return results, None
                m = cls.re_array_end.match(data, current_offset)
            return results, m.end()
        m = cls.re_null.match(data, offset)
        if m:
            return None, m.end()
        m = cls.re_true.match(data, offset)
        if m:
            return True, m.end()
        m = cls.re_false.match(data, offset)
        if m:
            return False, m.end()
        m = cls.re_name.match(data, offset)
        if m:
            return PdfName(cls.interpret_name(m.group(1))), m.end()
        m = cls.re_int.match(data, offset)
        if m:
            return int(m.group(1)), m.end()
        m = cls.re_real.match(data, offset)
        if m:
            # XXX Decimal instead of float???
            return float(m.group(1)), m.end()
        m = cls.re_string_hex.match(data, offset)
        if m:
            # filter out whitespace
            hex_string = bytearray(
                b for b in m.group(1) if b in b"0123456789abcdefABCDEF"
            )
            if len(hex_string) % 2 == 1:
                # append a 0 if the length is not even - yes, at the end
                hex_string.append(ord(b"0"))
            return bytearray.fromhex(hex_string.decode("us-ascii")), m.end()
        m = cls.re_string_lit.match(data, offset)
        if m:
            return cls.get_literal_string(data, m.end())
        # return None, offset  # fallback (only for debugging)
        msg = f"unrecognized object: {repr(data[offset : offset + 32])}"
        raise PdfFormatError(msg)
