    def __init__(self, op: str, lhs, rhs, queryables: dict[str, Any], encoding):
        super().__init__(op, lhs, rhs)
        self.queryables = queryables
        self.encoding = encoding
        self.condition = None
