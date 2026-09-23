    def shrink(self) -> None:
        super().shrink()
        self._update_metrics()
