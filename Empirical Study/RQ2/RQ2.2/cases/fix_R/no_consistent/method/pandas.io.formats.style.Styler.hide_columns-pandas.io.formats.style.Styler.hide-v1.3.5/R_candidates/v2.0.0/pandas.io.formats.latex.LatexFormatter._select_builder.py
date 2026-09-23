    def _select_builder(self) -> type[TableBuilderAbstract]:
        """Select proper table builder."""
        if self.longtable:
            return LongTableBuilder
        if any([self.caption, self.label, self.position]):
            return RegularTableBuilder
        return TabularBuilder
