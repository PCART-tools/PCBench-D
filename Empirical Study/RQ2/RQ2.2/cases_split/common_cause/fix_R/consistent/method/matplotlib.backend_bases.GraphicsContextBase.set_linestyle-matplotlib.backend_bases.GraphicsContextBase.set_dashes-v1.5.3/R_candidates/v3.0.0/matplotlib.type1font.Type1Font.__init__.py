    def __init__(self, input):
        """
        Initialize a Type-1 font. *input* can be either the file name of
        a pfb file or a 3-tuple of already-decoded Type-1 font parts.
        """
        if isinstance(input, tuple) and len(input) == 3:
            self.parts = input
        else:
            with open(input, 'rb') as file:
                data = self._read(file)
            self.parts = self._split(data)

        self._parse()
