    def _arg(self, nbytes, signed=False):
        """
        Read and return an integer argument *nbytes* long.
        Signedness is determined by the *signed* keyword.
        """
        str = self.file.read(nbytes)
        value = str[0]
        if signed and value >= 0x80:
            value = value - 0x100
        for i in range(1, nbytes):
            value = 0x100*value + str[i]
        return value
