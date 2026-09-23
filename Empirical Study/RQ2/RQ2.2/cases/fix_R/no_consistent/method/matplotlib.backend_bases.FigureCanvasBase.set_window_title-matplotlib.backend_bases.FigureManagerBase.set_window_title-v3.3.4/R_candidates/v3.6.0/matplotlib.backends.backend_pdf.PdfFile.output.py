    def output(self, *data):
        self.write(_fill([pdfRepr(x) for x in data]))
        self.write(b'\n')
