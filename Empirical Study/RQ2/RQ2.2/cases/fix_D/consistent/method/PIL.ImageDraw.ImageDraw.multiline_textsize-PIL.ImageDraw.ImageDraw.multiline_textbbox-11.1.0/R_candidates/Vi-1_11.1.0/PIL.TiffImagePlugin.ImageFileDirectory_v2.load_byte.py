    @_register_loader(1, 1)  # Basic type, except for the legacy API.
    def load_byte(self, data: bytes, legacy_api: bool = True) -> bytes:
        return data
