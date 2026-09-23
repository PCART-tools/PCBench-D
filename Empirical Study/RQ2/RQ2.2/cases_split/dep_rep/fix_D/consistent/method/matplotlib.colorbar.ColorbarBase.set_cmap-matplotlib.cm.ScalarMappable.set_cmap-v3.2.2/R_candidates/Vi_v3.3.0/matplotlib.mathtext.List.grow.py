    def grow(self):
        for child in self.children:
            child.grow()
        Box.grow(self)
        self.shift_amount *= GROW_FACTOR
        self.glue_set     *= GROW_FACTOR
