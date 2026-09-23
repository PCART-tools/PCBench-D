class BadStatusLine(HttpBadRequest):

    def __init__(self, line=''):
        if not line:
            line = repr(line)
        self.args = line,
        self.line = line
