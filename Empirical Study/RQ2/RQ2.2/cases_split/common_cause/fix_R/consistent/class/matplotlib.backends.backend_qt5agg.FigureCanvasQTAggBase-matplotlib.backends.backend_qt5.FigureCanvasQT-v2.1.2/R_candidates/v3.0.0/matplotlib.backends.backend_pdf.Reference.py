class Reference(object):
    """PDF reference object.
    Use PdfFile.reserveObject() to create References.
    """

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Reference %d>" % self.id

    def pdfRepr(self):
        return b"%d 0 R" % self.id

    def write(self, contents, file):
        write = file.write
        write(b"%d 0 obj\n" % self.id)
        write(pdfRepr(contents))
        write(b"\nendobj\n")
