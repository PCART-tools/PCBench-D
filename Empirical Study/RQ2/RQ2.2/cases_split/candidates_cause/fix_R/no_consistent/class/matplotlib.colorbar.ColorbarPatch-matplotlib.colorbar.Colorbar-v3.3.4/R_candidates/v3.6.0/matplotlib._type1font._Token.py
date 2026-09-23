class _Token:
    """
    A token in a PostScript stream.

    Attributes
    ----------
    pos : int
        Position, i.e. offset from the beginning of the data.
    raw : str
        Raw text of the token.
    kind : str
        Description of the token (for debugging or testing).
    """
    __slots__ = ('pos', 'raw')
    kind = '?'

    def __init__(self, pos, raw):
        _log.debug('type1font._Token %s at %d: %r', self.kind, pos, raw)
        self.pos = pos
        self.raw = raw

    def __str__(self):
        return f"<{self.kind} {self.raw} @{self.pos}>"

    def endpos(self):
        """Position one past the end of the token"""
        return self.pos + len(self.raw)

    def is_keyword(self, *names):
        """Is this a name token with one of the names?"""
        return False

    def is_slash_name(self):
        """Is this a name token that starts with a slash?"""
        return False

    def is_delim(self):
        """Is this a delimiter token?"""
        return False

    def is_number(self):
        """Is this a number token?"""
        return False

    def value(self):
        return self.raw
