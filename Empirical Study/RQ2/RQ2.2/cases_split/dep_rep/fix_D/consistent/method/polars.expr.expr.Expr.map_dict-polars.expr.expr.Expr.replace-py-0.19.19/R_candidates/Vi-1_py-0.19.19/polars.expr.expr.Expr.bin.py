    @property
    def bin(self) -> ExprBinaryNameSpace:
        """
        Create an object namespace of all binary related methods.

        See the individual method pages for full details
        """
        return ExprBinaryNameSpace(self)
