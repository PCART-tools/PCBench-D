    def shrink(self) -> None:
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            g = self.glue_spec
            self.glue_spec = g._replace(width=g.width * SHRINK_FACTOR)
