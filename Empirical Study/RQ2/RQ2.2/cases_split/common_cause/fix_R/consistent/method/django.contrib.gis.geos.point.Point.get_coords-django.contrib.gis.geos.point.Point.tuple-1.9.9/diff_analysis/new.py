    def get_coords(self):
        warnings.warn(
            "`get_coords()` is deprecated, use the `tuple` property instead.",
            RemovedInDjango20Warning, 2
        )
        return self.tuple
