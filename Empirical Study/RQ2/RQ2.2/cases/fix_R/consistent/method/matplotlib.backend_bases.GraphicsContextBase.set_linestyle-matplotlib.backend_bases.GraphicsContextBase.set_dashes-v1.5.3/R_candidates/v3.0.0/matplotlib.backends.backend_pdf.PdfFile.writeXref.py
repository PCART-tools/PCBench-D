    def writeXref(self):
        """Write out the xref table."""

        self.startxref = self.fh.tell() - self.tell_base
        self.write(b"xref\n0 %d\n" % self.nextObject)
        i = 0
        borken = False
        for offset, generation, name in self.xrefTable:
            if offset is None:
                print('No offset for object %d (%s)' % (i, name),
                      file=sys.stderr)
                borken = True
            else:
                key = b"f" if name == 'the zero object' else b"n"
                text = b"%010d %05d %b \n" % (offset, generation, key)
                self.write(text)
            i += 1
        if borken:
            raise AssertionError('Indirect object does not exist')
