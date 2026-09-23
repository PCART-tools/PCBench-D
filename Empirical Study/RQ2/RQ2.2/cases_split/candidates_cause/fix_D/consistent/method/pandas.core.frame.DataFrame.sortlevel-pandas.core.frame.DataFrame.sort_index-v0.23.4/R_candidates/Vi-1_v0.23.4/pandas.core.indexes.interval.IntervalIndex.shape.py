    @property
    def shape(self):
        # Avoid materializing self.values
        return self.left.shape
