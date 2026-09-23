    def _set_argtypes(self, argtypes):
        new_argtypes = [CONTEXT_PTR]
        new_argtypes.extend(argtypes)
        self.cfunc.argtypes = new_argtypes
