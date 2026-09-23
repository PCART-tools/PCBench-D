        def iter_any(self):
            """Returns an asynchronous iterator that yields slices of data
            as they come.

            Python-3.5 available for Python 3.5+ only
            """
            return AsyncStreamIterator(self.readany)
