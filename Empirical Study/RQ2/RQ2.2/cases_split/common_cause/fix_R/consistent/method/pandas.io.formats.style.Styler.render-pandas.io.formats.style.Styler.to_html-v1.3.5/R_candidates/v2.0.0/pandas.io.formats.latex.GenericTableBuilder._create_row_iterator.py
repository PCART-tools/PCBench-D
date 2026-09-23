    def _create_row_iterator(self, over: str) -> RowStringIterator:
        """Create iterator over header or body of the table.

        Parameters
        ----------
        over : {'body', 'header'}
            Over what to iterate.

        Returns
        -------
        RowStringIterator
            Iterator over body or header.
        """
        iterator_kind = self._select_iterator(over)
        return iterator_kind(
            formatter=self.fmt,
            multicolumn=self.multicolumn,
            multicolumn_format=self.multicolumn_format,
            multirow=self.multirow,
        )
