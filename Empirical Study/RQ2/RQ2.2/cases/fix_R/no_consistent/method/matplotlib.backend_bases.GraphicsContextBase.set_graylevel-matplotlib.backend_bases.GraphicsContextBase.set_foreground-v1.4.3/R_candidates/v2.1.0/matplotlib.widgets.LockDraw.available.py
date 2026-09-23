    def available(self, o):
        """drawing is available to *o*"""
        return not self.locked() or self.isowner(o)
