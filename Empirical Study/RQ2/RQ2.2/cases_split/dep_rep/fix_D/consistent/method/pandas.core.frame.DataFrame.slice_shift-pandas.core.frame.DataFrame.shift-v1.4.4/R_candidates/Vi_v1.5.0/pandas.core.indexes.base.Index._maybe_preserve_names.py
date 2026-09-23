    def _maybe_preserve_names(self, target: Index, preserve_names: bool):
        if preserve_names and target.nlevels == 1 and target.name != self.name:
            target = target.copy(deep=False)
            target.name = self.name
        return target
