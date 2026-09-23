    @property
    def size(self):
        # Avoid materializing self.values
        return self.left.size
