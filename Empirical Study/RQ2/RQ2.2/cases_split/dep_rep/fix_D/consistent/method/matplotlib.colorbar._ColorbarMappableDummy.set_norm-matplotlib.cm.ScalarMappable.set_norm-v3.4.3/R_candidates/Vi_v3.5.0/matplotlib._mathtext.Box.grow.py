    def grow(self):
        super().grow()
        self.width  *= GROW_FACTOR
        self.height *= GROW_FACTOR
        self.depth  *= GROW_FACTOR
