class _DelimiterToken(_Token):
    kind = 'delimiter'

    def is_delim(self):
        return True

    def opposite(self):
        return {'[': ']', ']': '[',
                '{': '}', '}': '{',
                '<<': '>>', '>>': '<<'
                }[self.raw]
