    def tolist(self) -> list:
        """
        Return a list of the underlying data.
        """
        return list(self.astype(object))
