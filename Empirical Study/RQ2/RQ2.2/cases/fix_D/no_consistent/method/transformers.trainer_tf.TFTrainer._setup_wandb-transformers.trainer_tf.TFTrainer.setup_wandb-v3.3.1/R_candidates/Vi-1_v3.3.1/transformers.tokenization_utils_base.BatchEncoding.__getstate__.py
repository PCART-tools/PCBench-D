    def __getstate__(self):
        return {"data": self.data, "encodings": self._encodings}
