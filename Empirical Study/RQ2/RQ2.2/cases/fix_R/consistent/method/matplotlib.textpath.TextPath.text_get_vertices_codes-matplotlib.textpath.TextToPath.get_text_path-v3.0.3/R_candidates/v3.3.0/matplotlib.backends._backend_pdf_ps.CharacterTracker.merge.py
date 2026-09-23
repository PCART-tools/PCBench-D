    def merge(self, other):
        """Update self with a font path to character codepoints."""
        for fname, charset in other.items():
            self.used.setdefault(fname, set()).update(charset)
