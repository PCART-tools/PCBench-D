    def _register_basic(idx_fmt_name):
        from .TiffTags import TYPES

        idx, fmt, name = idx_fmt_name
        TYPES[idx] = name
        size = struct.calcsize("=" + fmt)
        _load_dispatch[idx] = (  # noqa: F821
            size,
            lambda self, data, legacy_api=True: (
                self._unpack(f"{len(data) // size}{fmt}", data)
            ),
        )
        _write_dispatch[idx] = lambda self, *values: (  # noqa: F821
            b"".join(self._pack(fmt, value) for value in values)
        )
