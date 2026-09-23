    def __init__(self, *args):
        if not (len(args) % 2 == 0 and len(args) >= 2):
            raise ValueError(
                'Need to invoke as'
                'option_context(pat, val, [(pat, val), ...)).'
            )

        self.ops = list(zip(args[::2], args[1::2]))
