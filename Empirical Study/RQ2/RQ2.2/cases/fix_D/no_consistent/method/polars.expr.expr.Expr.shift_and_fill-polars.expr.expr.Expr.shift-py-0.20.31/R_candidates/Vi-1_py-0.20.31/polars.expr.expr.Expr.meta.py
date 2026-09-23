    @property
    def meta(self) -> ExprMetaNameSpace:
        """
        Create an object namespace of all meta related expression methods.

        This can be used to modify and traverse existing expressions.
        """
        return ExprMetaNameSpace(self)
