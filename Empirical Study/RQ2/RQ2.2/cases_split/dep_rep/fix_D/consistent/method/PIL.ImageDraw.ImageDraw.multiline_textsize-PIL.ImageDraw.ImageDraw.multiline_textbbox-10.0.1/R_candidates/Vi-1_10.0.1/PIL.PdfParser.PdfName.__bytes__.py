    def __bytes__(self):
        result = bytearray(b"/")
        for b in self.name:
            if b in self.allowed_chars:
                result.append(b)
            else:
                result.extend(b"#%02X" % b)
        return bytes(result)
