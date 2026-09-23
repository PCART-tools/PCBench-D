    def end_document(self):
        """Ends printing. (Write PostScript DSC footer.)"""
        self.fp.write(b"%%EndDocument\nrestore showpage\n%%End\n")
        if hasattr(self.fp, "flush"):
            self.fp.flush()
