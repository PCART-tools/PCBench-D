class BaseFinder:
    """
    A base file finder to be used for custom staticfiles finder classes.
    """
    def check(self, **kwargs):
        raise NotImplementedError(
            'subclasses may provide a check() method to verify the finder is '
            'configured correctly.'
        )

    def find(self, path, all=False):
        """
        Given a relative file path, find an absolute file path.

        If the ``all`` parameter is False (default) return only the first found
        file path; if True, return a list of all found files paths.
        """
        raise NotImplementedError('subclasses of BaseFinder must provide a find() method')

    def list(self, ignore_patterns):
        """
        Given an optional list of paths to ignore, return a two item iterable
        consisting of the relative path and storage instance.
        """
        raise NotImplementedError('subclasses of BaseFinder must provide a list() method')
