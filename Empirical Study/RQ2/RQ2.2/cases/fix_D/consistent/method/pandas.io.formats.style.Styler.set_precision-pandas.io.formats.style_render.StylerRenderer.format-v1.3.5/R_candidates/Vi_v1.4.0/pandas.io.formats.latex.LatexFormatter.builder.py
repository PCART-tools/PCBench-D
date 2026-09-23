    @property
    def builder(self) -> TableBuilderAbstract:
        """Concrete table builder.

        Returns
        -------
        TableBuilder
        """
        builder = self._select_builder()
        return builder(
            formatter=self.fmt,
            column_format=self.column_format,
            multicolumn=self.multicolumn,
            multicolumn_format=self.multicolumn_format,
            multirow=self.multirow,
            caption=self.caption,
            short_caption=self.short_caption,
            label=self.label,
            position=self.position,
        )
