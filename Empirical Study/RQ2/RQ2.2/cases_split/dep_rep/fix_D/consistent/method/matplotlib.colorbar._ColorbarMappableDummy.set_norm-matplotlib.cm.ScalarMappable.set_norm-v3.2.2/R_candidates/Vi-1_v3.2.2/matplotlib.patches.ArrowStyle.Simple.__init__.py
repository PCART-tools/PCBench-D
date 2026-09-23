        def __init__(self, head_length=.5, head_width=.5, tail_width=.2):
            """
            Parameters
            ----------
            head_length : float, optional, default : 0.5
                Length of the arrow head

            head_width : float, optional, default : 0.5
                Width of the arrow head

            tail_width : float, optional, default : 0.2
                Width of the arrow tail
            """
            self.head_length, self.head_width, self.tail_width = \
                head_length, head_width, tail_width
            super().__init__()
