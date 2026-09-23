    def _arg(self, nbytes, signed=False):
        """
        Read and return an integer argument *nbytes* long.
        Signedness is determined by the *signed* keyword.
        """
        buf = self.file.read(nbytes)
        value = buf[0]
        if signed and value >= 0x80:
            value = value - 0x100
        for b in buf[1:]:
            value = 0x100*value + b
        return value
