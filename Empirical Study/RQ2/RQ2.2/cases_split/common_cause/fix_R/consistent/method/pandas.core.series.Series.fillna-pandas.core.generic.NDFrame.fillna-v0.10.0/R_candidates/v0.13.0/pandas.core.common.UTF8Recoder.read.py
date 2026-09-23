    def read(self, bytes=-1):
        return self.reader.read(bytes).encode('utf-8')
