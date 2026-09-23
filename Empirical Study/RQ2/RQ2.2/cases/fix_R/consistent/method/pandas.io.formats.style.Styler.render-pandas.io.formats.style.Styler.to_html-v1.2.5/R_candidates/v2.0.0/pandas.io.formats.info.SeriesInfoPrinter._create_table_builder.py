    def _create_table_builder(self) -> SeriesTableBuilder:
        """
        Create instance of table builder based on verbosity.
        """
        if self.verbose or self.verbose is None:
            return SeriesTableBuilderVerbose(
                info=self.info,
                with_counts=self.show_counts,
            )
        else:
            return SeriesTableBuilderNonVerbose(info=self.info)
