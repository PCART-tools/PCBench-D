    def endpos(self):
        """Position one past the end of the token"""
        return self.pos + len(self.raw)
