@total_ordering
class Name:
    """PDF name object."""
    __slots__ = ('name',)
    _regex = re.compile(r'[^!-~]')

    def __init__(self, name):
        if isinstance(name, Name):
            self.name = name.name
        else:
            if isinstance(name, bytes):
                name = name.decode('ascii')
            self.name = self._regex.sub(Name.hexify, name).encode('ascii')

    def __repr__(self):
        return "<Name %s>" % self.name

    def __str__(self):
        return '/' + str(self.name)

    def __eq__(self, other):
        return isinstance(other, Name) and self.name == other.name

    def __lt__(self, other):
        return isinstance(other, Name) and self.name < other.name

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def hexify(match):
        return '#%02x' % ord(match.group())

    def pdfRepr(self):
        return b'/' + self.name
