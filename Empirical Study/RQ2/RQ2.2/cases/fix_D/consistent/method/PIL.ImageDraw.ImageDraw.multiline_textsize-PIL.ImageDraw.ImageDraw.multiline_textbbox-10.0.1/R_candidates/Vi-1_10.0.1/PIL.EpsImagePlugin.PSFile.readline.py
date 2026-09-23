    def readline(self):
        s = [self.char or b""]
        self.char = None

        c = self.fp.read(1)
        while (c not in b"\r\n") and len(c):
            s.append(c)
            c = self.fp.read(1)

        self.char = self.fp.read(1)
        # line endings can be 1 or 2 of \r \n, in either order
        if self.char in b"\r\n":
            self.char = None

        return b"".join(s).decode("latin-1")
