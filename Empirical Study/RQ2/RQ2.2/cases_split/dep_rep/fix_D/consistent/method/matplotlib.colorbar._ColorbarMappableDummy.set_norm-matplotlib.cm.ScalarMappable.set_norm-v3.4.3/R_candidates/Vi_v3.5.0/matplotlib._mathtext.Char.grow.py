    def grow(self):
        super().grow()
        self.fontsize *= GROW_FACTOR
        self.width    *= GROW_FACTOR
        self.height   *= GROW_FACTOR
        self.depth    *= GROW_FACTOR
