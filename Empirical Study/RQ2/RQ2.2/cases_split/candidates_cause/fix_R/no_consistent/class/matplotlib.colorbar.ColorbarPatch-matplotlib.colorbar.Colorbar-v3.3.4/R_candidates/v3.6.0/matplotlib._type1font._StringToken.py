class _StringToken(_Token):
    kind = 'string'
    _escapes_re = re.compile(r'\\([\\()nrtbf]|[0-7]{1,3})')
    _replacements = {'\\': '\\', '(': '(', ')': ')', 'n': '\n',
                     'r': '\r', 't': '\t', 'b': '\b', 'f': '\f'}
    _ws_re = re.compile('[\0\t\r\f\n ]')

    @classmethod
    def _escape(cls, match):
        group = match.group(1)
        try:
            return cls._replacements[group]
        except KeyError:
            return chr(int(group, 8))

    @functools.lru_cache()
    def value(self):
        if self.raw[0] == '(':
            return self._escapes_re.sub(self._escape, self.raw[1:-1])
        else:
            data = self._ws_re.sub('', self.raw[1:-1])
            if len(data) % 2 == 1:
                data += '0'
            return binascii.unhexlify(data)
