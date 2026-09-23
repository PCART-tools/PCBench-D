    def grow(self):
        Node.grow(self)
        g = self.glue_spec
        self.glue_spec = g._replace(width=g.width * GROW_FACTOR)
