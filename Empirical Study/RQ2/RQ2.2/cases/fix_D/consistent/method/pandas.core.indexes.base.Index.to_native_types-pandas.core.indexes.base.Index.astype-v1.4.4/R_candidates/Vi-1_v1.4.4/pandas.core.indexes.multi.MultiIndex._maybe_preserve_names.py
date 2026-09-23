    def _maybe_preserve_names(self, target: Index, preserve_names: bool) -> Index:
        if (
            preserve_names
            and target.nlevels == self.nlevels
            and target.names != self.names
        ):
            target = target.copy(deep=False)
            target.names = self.names
        return target
