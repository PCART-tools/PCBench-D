    def __init__(self, elements: T.Sequence[Node]):
        super().__init__(0., 0., 0.)
        self.shift_amount = 0.   # An arbitrary offset
        self.children = [*elements]  # The child nodes of this list
        # The following parameters are set in the vpack and hpack functions
        self.glue_set     = 0.   # The glue setting of this list
        self.glue_sign    = 0    # 0: normal, -1: shrinking, 1: stretching
        self.glue_order   = 0    # The order of infinity (0 - 3) for the glue
