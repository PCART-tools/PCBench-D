        def __init__(self, tail_width=.3, shrink_factor=0.5):
            """
            Parameters
            ----------
            tail_width : float, optional, default : 0.3
                Width of the tail

            shrink_factor : float, optional, default : 0.5
                Fraction of the arrow width at the middle point
            """
            self.tail_width = tail_width
            self.shrink_factor = shrink_factor
            super().__init__()
