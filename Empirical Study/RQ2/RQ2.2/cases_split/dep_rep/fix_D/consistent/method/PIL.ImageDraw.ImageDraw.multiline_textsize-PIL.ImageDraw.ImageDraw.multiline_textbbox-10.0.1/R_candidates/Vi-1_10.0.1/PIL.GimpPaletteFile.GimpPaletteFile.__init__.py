    def __init__(self, fp):
        self.palette = [o8(i) * 3 for i in range(256)]

        if fp.readline()[:12] != b"GIMP Palette":
            msg = "not a GIMP palette file"
            raise SyntaxError(msg)

        for i in range(256):
            s = fp.readline()
            if not s:
                break

            # skip fields and comment lines
            if re.match(rb"\w+:|#", s):
                continue
            if len(s) > 100:
                msg = "bad palette file"
                raise SyntaxError(msg)

            v = tuple(map(int, s.split()[:3]))
            if len(v) != 3:
                msg = "bad palette entry"
                raise ValueError(msg)

            self.palette[i] = o8(v[0]) + o8(v[1]) + o8(v[2])

        self.palette = b"".join(self.palette)
