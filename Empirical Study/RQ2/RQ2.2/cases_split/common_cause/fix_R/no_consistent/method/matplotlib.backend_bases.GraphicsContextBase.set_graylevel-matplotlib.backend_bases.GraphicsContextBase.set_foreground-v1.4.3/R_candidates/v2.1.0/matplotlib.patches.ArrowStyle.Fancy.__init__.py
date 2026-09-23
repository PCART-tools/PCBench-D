        def __init__(self, head_length=.4, head_width=.4, tail_width=.4):
            """
            Parameters
            ----------
            head_length : float, optional, default : 0.4
                Length of the arrow head

            head_width : float, optional, default : 0.4
                Width of the arrow head

            tail_width : float, optional, default : 0.4
                Width of the arrow tail
            """

            self.head_length, self.head_width, self.tail_width = \
                head_length, head_width, tail_width
            super(ArrowStyle.Fancy, self).__init__()
