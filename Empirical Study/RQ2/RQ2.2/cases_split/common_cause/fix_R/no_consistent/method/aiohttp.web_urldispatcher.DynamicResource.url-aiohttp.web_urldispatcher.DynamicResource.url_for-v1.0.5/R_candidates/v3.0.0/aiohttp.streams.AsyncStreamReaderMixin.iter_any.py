    def iter_any(self):
        """Returns an asynchronous iterator that yields all the available
        data as soon as it is received

        Python-3.5 available for Python 3.5+ only
        """
        return AsyncStreamIterator(self.readany)
