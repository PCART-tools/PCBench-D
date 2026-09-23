    def _expect(self, s):
        exp = s.encode("utf8")
        buf = bytearray()
        while True:
            b = self.latex.stdout.read(1)
            buf += b
            if buf[-len(exp):] == exp:
                break
            if not len(b):
                self.latex.kill()
                self.latex = None
                raise LatexError("LaTeX process halted", buf.decode("utf8"))
        return buf.decode("utf8")
