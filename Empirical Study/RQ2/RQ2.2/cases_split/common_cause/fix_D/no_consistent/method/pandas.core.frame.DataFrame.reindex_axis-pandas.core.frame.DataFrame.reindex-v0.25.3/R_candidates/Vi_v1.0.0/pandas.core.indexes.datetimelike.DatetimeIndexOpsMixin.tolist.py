    def tolist(self) -> List:
        """
        Return a list of the underlying data.
        """
        return list(self.astype(object))
