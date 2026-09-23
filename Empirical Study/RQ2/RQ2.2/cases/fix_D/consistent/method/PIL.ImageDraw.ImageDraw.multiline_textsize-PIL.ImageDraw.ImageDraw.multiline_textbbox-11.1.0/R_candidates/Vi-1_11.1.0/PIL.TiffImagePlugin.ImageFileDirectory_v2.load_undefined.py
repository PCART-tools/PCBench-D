    @_register_loader(7, 1)
    def load_undefined(self, data: bytes, legacy_api: bool = True) -> bytes:
        return data
