    def __bytes__(self):
        return b"<%s>" % b"".join(b"%02X" % b for b in self.data)
