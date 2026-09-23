    def write(self, contents, file):
        write = file.write
        write(("%d 0 obj\n" % self.id).encode('ascii'))
        write(pdfRepr(contents))
        write(b"\nendobj\n")
