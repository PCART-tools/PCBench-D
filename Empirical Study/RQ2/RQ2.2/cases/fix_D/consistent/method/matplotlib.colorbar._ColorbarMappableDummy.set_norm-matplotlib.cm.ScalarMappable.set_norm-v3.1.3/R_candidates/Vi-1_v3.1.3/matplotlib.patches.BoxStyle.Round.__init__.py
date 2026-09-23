        def __init__(self, pad=0.3, rounding_size=None):
            """
            *pad*
              amount of padding

            *rounding_size*
              rounding radius of corners. *pad* if None
            """
            self.pad = pad
            self.rounding_size = rounding_size
            super().__init__()
