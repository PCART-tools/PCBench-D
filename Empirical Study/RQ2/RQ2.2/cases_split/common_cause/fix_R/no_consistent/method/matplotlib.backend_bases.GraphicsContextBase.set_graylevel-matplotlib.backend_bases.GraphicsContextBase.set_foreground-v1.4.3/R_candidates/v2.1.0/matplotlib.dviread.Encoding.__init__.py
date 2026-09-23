    def __init__(self, filename):
        with open(filename, 'rb') as file:
            matplotlib.verbose.report('Parsing TeX encoding ' + filename,
                                      'debug-annoying')
            self.encoding = self._parse(file)
            matplotlib.verbose.report('Result: ' + repr(self.encoding),
                                      'debug-annoying')
