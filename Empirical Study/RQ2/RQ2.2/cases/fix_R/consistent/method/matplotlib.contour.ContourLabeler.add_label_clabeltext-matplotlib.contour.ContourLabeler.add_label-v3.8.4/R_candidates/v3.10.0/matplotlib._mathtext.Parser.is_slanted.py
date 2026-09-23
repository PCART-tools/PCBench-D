    def is_slanted(self, nucleus: Node) -> bool:
        if isinstance(nucleus, Char):
            return nucleus.is_slanted()
        return False
