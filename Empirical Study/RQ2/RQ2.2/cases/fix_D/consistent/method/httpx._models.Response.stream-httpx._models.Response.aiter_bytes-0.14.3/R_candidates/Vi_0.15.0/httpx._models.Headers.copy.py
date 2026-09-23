    def copy(self) -> "Headers":
        return Headers(dict(self.items()), encoding=self.encoding)
