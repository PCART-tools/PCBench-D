    @_register_loader(2, 1)
    def load_string(self, data: bytes, legacy_api: bool = True) -> str:
        if data.endswith(b"\0"):
            data = data[:-1]
        return data.decode("latin-1", "replace")
