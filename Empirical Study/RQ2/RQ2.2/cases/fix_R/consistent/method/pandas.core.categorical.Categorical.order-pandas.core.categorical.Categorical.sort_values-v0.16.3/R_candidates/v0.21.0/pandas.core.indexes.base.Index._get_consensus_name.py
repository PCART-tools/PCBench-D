    def _get_consensus_name(self, other):
        """
        Given 2 indexes, give a consensus name meaning
        we take the not None one, or None if the names differ.
        Return a new object if we are resetting the name
        """
        if self.name != other.name:
            if self.name is None or other.name is None:
                name = self.name or other.name
            else:
                name = None
            if self.name != name:
                return self._shallow_copy(name=name)
        return self
