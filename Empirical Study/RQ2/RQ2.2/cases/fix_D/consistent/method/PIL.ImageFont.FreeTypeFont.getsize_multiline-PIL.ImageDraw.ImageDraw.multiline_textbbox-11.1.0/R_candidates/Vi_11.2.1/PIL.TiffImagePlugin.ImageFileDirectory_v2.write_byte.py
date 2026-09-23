    @_register_writer(1)  # Basic type, except for the legacy API.
    def write_byte(self, data: bytes | int | IFDRational) -> bytes:
        if isinstance(data, IFDRational):
            data = int(data)
        if isinstance(data, int):
            data = bytes((data,))
        return data
