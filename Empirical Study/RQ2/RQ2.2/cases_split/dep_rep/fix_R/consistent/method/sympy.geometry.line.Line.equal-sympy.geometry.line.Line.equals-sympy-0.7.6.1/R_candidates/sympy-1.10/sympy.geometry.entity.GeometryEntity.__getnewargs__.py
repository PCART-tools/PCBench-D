    def __getnewargs__(self):
        """Returns a tuple that will be passed to __new__ on unpickling."""
        return tuple(self.args)
