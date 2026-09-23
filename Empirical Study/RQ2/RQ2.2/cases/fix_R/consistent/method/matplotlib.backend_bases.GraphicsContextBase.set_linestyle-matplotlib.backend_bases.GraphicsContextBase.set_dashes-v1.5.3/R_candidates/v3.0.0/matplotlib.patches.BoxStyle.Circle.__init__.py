        def __init__(self, pad=0.3):
            """
            Parameters
            ----------
            pad : float
                The amount of padding around the original box.
            """
            self.pad = pad
            super().__init__()
