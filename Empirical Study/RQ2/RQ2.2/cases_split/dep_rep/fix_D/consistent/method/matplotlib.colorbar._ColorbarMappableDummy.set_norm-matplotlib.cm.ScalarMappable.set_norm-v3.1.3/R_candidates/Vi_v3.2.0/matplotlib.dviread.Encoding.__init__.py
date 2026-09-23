    def __init__(self, filename):
        with open(filename, 'rb') as file:
            _log.debug('Parsing TeX encoding %s', filename)
            self.encoding = self._parse(file)
            _log.debug('Result: %s', self.encoding)
