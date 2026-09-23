        def __init__(self, pad=0.3, rounding_size=None):
            """
            *pad*
              amount of padding

            *rounding_size*
              rounding size of edges. *pad* if None
            """
            self.pad = pad
            self.rounding_size = rounding_size
            super().__init__()
