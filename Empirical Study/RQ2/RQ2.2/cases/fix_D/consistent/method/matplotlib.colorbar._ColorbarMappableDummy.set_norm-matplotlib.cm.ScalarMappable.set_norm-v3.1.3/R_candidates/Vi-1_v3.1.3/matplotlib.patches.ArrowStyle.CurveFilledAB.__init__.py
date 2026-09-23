        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, optional, default : 0.4
                Length of the arrow head

            head_width : float, optional, default : 0.2
                Width of the arrow head
            """
            super().__init__(beginarrow=True, endarrow=True,
                             fillbegin=True, fillend=True,
                             head_length=head_length, head_width=head_width)
