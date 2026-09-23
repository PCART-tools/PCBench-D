    def __init__(self, base, offset):
        'place ticks on the i-th data points where (i-offset)%base==0'
        self._base = base
        self.offset = offset
