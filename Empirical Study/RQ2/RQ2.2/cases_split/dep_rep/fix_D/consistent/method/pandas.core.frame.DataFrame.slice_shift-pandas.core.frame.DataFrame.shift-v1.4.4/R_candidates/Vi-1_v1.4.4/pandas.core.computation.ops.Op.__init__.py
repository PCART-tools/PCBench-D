    def __init__(self, op: str, operands: Iterable[Term | Op], encoding=None):
        self.op = _bool_op_map.get(op, op)
        self.operands = operands
        self.encoding = encoding
