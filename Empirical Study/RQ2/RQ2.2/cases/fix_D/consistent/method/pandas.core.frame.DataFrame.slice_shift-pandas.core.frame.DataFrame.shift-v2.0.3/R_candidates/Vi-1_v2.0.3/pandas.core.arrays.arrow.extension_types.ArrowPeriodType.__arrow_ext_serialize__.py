    def __arrow_ext_serialize__(self) -> bytes:
        metadata = {"freq": self.freq}
        return json.dumps(metadata).encode()
