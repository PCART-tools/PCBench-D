    @property
    def _is_unique(self) -> bool:
        return len(unique1d(self.asi8.ravel("K"))) == self.size
