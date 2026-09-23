    def __init__(self, op, operands, *args, **kwargs):
        self.op = _bool_op_map.get(op, op)
        self.operands = operands
        self.encoding = kwargs.get('encoding', None)
