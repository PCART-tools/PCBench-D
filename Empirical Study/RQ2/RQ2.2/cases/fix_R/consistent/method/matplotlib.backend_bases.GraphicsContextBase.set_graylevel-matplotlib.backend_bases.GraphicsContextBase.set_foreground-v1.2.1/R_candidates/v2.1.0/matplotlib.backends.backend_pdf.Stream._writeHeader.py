    def _writeHeader(self):
        write = self.file.write
        write(("%d 0 obj\n" % self.id).encode('ascii'))
        dict = self.extra
        dict['Length'] = self.len
        if rcParams['pdf.compression']:
            dict['Filter'] = Name('FlateDecode')

        write(pdfRepr(dict))
        write(b"\nstream\n")
