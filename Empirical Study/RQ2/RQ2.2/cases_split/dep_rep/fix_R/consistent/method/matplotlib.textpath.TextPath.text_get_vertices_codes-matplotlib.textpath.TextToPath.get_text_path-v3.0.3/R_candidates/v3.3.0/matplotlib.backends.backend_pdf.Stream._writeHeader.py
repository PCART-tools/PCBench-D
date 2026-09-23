    def _writeHeader(self):
        write = self.file.write
        write(b"%d 0 obj\n" % self.id)
        dict = self.extra
        dict['Length'] = self.len
        if mpl.rcParams['pdf.compression']:
            dict['Filter'] = Name('FlateDecode')

        write(pdfRepr(dict))
        write(b"\nstream\n")
