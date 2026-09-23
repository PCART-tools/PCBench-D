    def grow(self):
        super().grow()
        g = self.glue_spec
        self.glue_spec = g._replace(width=g.width * GROW_FACTOR)
