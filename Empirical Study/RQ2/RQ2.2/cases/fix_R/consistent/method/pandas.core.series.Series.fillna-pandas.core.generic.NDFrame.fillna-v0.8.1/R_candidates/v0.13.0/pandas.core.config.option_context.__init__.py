    def __init__(self, *args):
        if not (len(args) % 2 == 0 and len(args) >= 2):
            raise AssertionError(
                'Need to invoke as'
                'option_context(pat, val, [(pat, val), ...)).'
            )

        ops = list(zip(args[::2], args[1::2]))
        undo = []
        for pat, val in ops:
            undo.append((pat, _get_option(pat, silent=True)))

        self.undo = undo

        for pat, val in ops:
            _set_option(pat, val, silent=True)
