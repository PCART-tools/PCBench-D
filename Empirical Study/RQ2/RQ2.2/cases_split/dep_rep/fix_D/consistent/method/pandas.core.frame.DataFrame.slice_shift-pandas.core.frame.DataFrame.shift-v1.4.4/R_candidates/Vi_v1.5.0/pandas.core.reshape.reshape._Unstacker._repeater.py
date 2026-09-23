    @cache_readonly
    def _repeater(self) -> np.ndarray:
        # The two indices differ only if the unstacked level had unused items:
        if len(self.removed_level_full) != len(self.removed_level):
            # In this case, we remap the new codes to the original level:
            repeater = self.removed_level_full.get_indexer(self.removed_level)
            if self.lift:
                repeater = np.insert(repeater, 0, -1)
        else:
            # Otherwise, we just use each level item exactly once:
            stride = len(self.removed_level) + self.lift
            repeater = np.arange(stride) - self.lift

        return repeater
