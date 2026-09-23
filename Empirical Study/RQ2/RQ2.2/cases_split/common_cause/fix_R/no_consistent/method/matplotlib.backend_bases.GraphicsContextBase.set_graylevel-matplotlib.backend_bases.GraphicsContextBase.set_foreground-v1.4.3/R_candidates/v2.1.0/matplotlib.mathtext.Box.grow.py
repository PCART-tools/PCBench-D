    def grow(self):
        Node.grow(self)
        self.width  *= GROW_FACTOR
        self.height *= GROW_FACTOR
        self.depth  *= GROW_FACTOR
