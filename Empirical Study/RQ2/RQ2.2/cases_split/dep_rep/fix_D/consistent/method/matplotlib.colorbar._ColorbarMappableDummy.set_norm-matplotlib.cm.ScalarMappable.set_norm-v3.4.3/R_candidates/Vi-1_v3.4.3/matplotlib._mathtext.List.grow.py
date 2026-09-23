    def grow(self):
        for child in self.children:
            child.grow()
        super().grow()
        self.shift_amount *= GROW_FACTOR
        self.glue_set     *= GROW_FACTOR
