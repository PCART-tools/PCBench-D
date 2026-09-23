    @_register_writer(2)
    def write_string(self, value: str | bytes | int) -> bytes:
        # remerge of https://github.com/python-pillow/Pillow/pull/1416
        if isinstance(value, int):
            value = str(value)
        if not isinstance(value, bytes):
            value = value.encode("ascii", "replace")
        return value + b"\0"
