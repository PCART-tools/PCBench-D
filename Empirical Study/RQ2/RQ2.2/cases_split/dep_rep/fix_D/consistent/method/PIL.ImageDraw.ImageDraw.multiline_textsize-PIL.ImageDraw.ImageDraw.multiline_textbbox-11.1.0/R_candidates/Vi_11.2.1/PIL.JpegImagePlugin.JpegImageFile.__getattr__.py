    def __getattr__(self, name: str) -> Any:
        if name in ("huffman_ac", "huffman_dc"):
            deprecate(name, 12)
            return getattr(self, "_" + name)
        raise AttributeError(name)
