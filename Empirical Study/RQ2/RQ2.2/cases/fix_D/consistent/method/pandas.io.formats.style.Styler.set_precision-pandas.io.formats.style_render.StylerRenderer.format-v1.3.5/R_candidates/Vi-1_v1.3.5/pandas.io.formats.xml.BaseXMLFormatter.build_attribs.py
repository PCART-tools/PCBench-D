    def build_attribs(self) -> None:
        """
        Create attributes of row.

        This method adds attributes using attr_cols to row element and
        works with tuples for multindex or hierarchical columns.
        """

        raise AbstractMethodError(self)
