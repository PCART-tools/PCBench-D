    def _formatter(self, boxed=False):
        if boxed:
            return str
        return "'{}'".format
