        def __init__(self, pad=0.3, tooth_size=None):
            """
            *pad*
              amount of padding

            *tooth_size*
              size of the sawtooth. pad* if None
            """
            self.pad = pad
            self.tooth_size = tooth_size
            super(BoxStyle.Sawtooth, self).__init__()
