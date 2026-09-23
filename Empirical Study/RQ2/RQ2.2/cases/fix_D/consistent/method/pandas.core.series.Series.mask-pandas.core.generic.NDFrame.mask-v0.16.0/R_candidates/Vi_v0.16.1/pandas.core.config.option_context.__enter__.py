    def __enter__(self):
        undo = []
        for pat, val in self.ops:
            undo.append((pat, _get_option(pat, silent=True)))

        self.undo = undo

        for pat, val in self.ops:
            _set_option(pat, val, silent=True)
