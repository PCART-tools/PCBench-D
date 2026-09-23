@total_ordering
class Name:
    """PDF name object."""
    __slots__ = ('name',)
    _hexify = {c: '#%02x' % c
               for c in {*range(256)} - {*range(ord('!'), ord('~') + 1)}}

    def __init__(self, name):
        if isinstance(name, Name):
            self.name = name.name
        else:
            if isinstance(name, bytes):
                name = name.decode('ascii')
            self.name = name.translate(self._hexify).encode('ascii')

    def __repr__(self):
        return "<Name %s>" % self.name

    def __str__(self):
        return '/' + self.name.decode('ascii')

    def __eq__(self, other):
        return isinstance(other, Name) and self.name == other.name

    def __lt__(self, other):
        return isinstance(other, Name) and self.name < other.name

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    @_api.deprecated("3.6")
    def hexify(match):
        return '#%02x' % ord(match.group())

    def pdfRepr(self):
        return b'/' + self.name
