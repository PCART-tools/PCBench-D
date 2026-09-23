    def recordXref(self, id):
        self.xrefTable[id][0] = self.fh.tell() - self.tell_base
