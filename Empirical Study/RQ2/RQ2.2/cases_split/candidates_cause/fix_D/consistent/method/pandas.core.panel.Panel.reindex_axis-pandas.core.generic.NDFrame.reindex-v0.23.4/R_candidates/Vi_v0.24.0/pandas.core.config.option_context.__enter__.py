    def __enter__(self):
        self.undo = [(pat, _get_option(pat, silent=True))
                     for pat, val in self.ops]

        for pat, val in self.ops:
            _set_option(pat, val, silent=True)
