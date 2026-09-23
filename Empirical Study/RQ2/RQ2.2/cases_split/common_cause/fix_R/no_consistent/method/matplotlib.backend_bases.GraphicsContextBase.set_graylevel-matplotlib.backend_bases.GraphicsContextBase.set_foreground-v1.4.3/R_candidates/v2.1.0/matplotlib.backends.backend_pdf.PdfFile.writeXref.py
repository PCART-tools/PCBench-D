    def writeXref(self):
        """Write out the xref table."""

        self.startxref = self.fh.tell() - self.tell_base
        self.write(("xref\n0 %d\n" % self.nextObject).encode('ascii'))
        i = 0
        borken = False
        for offset, generation, name in self.xrefTable:
            if offset is None:
                print('No offset for object %d (%s)' % (i, name),
                      file=sys.stderr)
                borken = True
            else:
                if name == 'the zero object':
                    key = "f"
                else:
                    key = "n"
                text = "%010d %05d %s \n" % (offset, generation, key)
                self.write(text.encode('ascii'))
            i += 1
        if borken:
            raise AssertionError('Indirect object does not exist')
