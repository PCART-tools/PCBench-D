    @_register_writer(7)
    def write_undefined(self, value):
        if isinstance(value, int):
            value = str(value).encode("ascii", "replace")
        return value
