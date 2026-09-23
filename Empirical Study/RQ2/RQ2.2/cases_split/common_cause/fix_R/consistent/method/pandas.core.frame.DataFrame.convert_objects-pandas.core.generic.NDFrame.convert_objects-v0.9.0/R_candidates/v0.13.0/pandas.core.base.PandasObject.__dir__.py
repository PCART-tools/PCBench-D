    def __dir__(self):
        """
        Provide method name lookup and completion
        Only provide 'public' methods
        """
        return list(sorted(list(set(dir(type(self)) + self._local_dir()))))
