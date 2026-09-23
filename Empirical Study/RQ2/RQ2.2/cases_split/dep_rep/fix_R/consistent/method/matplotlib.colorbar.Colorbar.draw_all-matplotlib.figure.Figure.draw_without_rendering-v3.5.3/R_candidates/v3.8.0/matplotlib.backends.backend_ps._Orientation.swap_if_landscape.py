    def swap_if_landscape(self, shape):
        return shape[::-1] if self.name == "landscape" else shape
