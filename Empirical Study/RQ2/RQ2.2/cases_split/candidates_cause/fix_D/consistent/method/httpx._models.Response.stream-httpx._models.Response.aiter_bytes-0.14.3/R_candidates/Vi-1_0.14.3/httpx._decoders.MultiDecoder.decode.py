    def decode(self, data: bytes) -> bytes:
        for child in self.children:
            data = child.decode(data)
        return data
