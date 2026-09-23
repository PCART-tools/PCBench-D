    def __exit__(self, *args):
        if self.undo:
            for pat, val in self.undo:
                _set_option(pat, val, silent=True)
