        def iter_chunked(self, n):
            """Returns an asynchronous iterator that yields chunks of size n.

            Python-3.5 available for Python 3.5+ only
            """
            return AsyncStreamIterator(lambda: self.read(n))
