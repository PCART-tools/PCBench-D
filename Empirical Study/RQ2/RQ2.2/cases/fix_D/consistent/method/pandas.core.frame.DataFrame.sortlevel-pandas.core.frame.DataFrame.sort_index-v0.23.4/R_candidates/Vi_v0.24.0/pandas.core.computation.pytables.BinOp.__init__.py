    def __init__(self, op, lhs, rhs, queryables, encoding):
        super(BinOp, self).__init__(op, lhs, rhs)
        self.queryables = queryables
        self.encoding = encoding
        self.filter = None
        self.condition = None
