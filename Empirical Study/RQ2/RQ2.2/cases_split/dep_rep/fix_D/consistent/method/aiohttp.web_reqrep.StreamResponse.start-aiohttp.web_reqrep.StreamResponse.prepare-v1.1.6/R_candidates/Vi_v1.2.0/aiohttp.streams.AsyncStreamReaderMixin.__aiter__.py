        def __aiter__(self):
            return AsyncStreamIterator(self.readline)
