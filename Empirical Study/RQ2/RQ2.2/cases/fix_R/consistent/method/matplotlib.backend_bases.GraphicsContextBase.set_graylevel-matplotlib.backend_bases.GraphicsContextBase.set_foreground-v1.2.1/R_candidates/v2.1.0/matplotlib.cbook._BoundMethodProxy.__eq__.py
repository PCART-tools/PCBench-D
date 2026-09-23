    def __eq__(self, other):
        """
        Compare the held function and instance with that held by
        another proxy.
        """
        try:
            if self.inst is None:
                return self.func == other.func and other.inst is None
            else:
                return self.func == other.func and self.inst() == other.inst()
        except Exception:
            return False
