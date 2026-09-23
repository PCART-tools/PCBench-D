    def _formatter(self, boxed: bool = False):
        if boxed:
            return str
        return "'{}'".format
