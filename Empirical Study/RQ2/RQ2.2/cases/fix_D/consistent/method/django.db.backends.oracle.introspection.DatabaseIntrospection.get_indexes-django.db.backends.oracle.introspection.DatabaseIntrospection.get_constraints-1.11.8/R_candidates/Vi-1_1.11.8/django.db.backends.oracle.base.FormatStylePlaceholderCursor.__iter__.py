    def __iter__(self):
        return CursorIterator(self.cursor)
