@_api.deprecated("3.3")
class Encoding:
    r"""
    Parse a \*.enc file referenced from a psfonts.map style file.

    The format this class understands is a very limited subset of PostScript.

    Usage (subject to change)::

      for name in Encoding(filename):
          whatever(name)

    Parameters
    ----------
    filename : str or path-like

    Attributes
    ----------
    encoding : list
        List of character names
    """
    __slots__ = ('encoding',)

    def __init__(self, filename):
        with open(filename, 'rb') as file:
            _log.debug('Parsing TeX encoding %s', filename)
            self.encoding = self._parse(file)
            _log.debug('Result: %s', self.encoding)

    def __iter__(self):
        yield from self.encoding

    @staticmethod
    def _parse(file):
        lines = (line.split(b'%', 1)[0].strip() for line in file)
        data = b''.join(lines)
        beginning = data.find(b'[')
        if beginning < 0:
            raise ValueError("Cannot locate beginning of encoding in {}"
                             .format(file))
        data = data[beginning:]
        end = data.find(b']')
        if end < 0:
            raise ValueError("Cannot locate end of encoding in {}"
                             .format(file))
        data = data[:end]
        return re.findall(br'/([^][{}<>\s]+)', data)
