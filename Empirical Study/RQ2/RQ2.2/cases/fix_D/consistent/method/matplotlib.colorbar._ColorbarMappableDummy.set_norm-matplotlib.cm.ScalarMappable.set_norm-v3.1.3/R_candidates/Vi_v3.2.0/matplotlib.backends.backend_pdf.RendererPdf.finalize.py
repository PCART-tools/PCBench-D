    def finalize(self):
        self.file.output(*self.gc.finalize())
