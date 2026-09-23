    def shrink(self) -> None:
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            self.width *= SHRINK_FACTOR
