    def output(self, *data):
        self.write(fill([pdfRepr(x) for x in data]))
        self.write(b'\n')
