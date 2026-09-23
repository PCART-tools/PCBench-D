    def _create_table_builder(self) -> DataFrameTableBuilder:
        """
        Create instance of table builder based on verbosity and display settings.
        """
        if self.verbose:
            return DataFrameTableBuilderVerbose(
                info=self.info,
                with_counts=self.show_counts,
            )
        elif self.verbose is False:  # specifically set to False, not necessarily None
            return DataFrameTableBuilderNonVerbose(info=self.info)
        elif self.exceeds_info_cols:
            return DataFrameTableBuilderNonVerbose(info=self.info)
        else:
            return DataFrameTableBuilderVerbose(
                info=self.info,
                with_counts=self.show_counts,
            )
