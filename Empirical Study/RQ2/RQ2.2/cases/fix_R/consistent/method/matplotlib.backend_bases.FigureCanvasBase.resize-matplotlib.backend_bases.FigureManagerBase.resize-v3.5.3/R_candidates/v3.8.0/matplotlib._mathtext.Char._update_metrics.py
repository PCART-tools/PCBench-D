    def _update_metrics(self) -> None:
        metrics = self._metrics = self.fontset.get_metrics(
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
        if self.c == ' ':
            self.width = metrics.advance
        else:
            self.width = metrics.width
        self.height = metrics.iceberg
        self.depth = -(metrics.iceberg - metrics.height)
