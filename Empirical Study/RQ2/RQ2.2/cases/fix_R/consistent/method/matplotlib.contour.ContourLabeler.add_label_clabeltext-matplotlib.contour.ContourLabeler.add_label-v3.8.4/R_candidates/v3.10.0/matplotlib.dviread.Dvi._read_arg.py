    def _read_arg(self, nbytes, signed=False):
        """
        Read and return a big-endian integer *nbytes* long.
        Signedness is determined by the *signed* keyword.
        """
        return int.from_bytes(self.file.read(nbytes), "big", signed=signed)
