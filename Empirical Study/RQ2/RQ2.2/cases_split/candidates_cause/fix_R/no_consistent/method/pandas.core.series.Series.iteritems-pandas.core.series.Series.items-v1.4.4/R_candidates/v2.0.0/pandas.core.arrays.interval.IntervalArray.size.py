    @property
    def size(self) -> int:
        # Avoid materializing self.values
        return self.left.size
