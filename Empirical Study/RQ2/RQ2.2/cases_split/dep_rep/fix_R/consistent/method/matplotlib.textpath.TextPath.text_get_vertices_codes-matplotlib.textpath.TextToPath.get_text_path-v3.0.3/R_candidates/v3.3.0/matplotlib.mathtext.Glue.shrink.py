    def shrink(self):
        Node.shrink(self)
        if self.size < NUM_SIZE_LEVELS:
            g = self.glue_spec
            self.glue_spec = g._replace(width=g.width * SHRINK_FACTOR)
