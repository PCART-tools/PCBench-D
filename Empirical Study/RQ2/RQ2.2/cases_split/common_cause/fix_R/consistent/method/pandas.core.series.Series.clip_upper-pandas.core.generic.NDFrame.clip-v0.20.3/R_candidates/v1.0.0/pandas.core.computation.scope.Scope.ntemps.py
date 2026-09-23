    @property
    def ntemps(self) -> int:
        """The number of temporary variables in this scope"""
        return len(self.temps)
