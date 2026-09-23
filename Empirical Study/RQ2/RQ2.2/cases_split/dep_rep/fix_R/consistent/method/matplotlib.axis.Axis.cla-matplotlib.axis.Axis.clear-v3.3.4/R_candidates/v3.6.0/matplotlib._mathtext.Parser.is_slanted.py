    def is_slanted(self, nucleus):
        if isinstance(nucleus, Char):
            return nucleus.is_slanted()
        return False
