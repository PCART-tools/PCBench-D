    @property
    def name(self) -> ExprNameNameSpace:
        """
        Create an object namespace of all expressions that modify expression names.

        See the individual method pages for full details.
        """
        return ExprNameNameSpace(self)
