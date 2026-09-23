@_api.deprecated("3.6")
class Operator:
    __slots__ = ('op',)

    def __init__(self, op):
        self.op = op

    def __repr__(self):
        return '<Operator %s>' % self.op

    def pdfRepr(self):
        return self.op
