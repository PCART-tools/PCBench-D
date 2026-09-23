    class SeekableFile(object):
        def __init__(self, file):
            if isinstance(file, SeekableFile):  # idempotent
                file = file.file
            self.file = file

        def seekable(self):
            return True

        def readable(self):
            try:
                return self.file.readable()
            except AttributeError:
                return 'r' in self.file.mode

        def writable(self):
            try:
                return self.file.writable()
            except AttributeError:
                return 'w' in self.file.mode

        def read1(self, *args, **kwargs):  # https://bugs.python.org/issue12591
            return self.file.read(*args, **kwargs)

        def __iter__(self):
            return self.file.__iter__()

        def __getattr__(self, key):
            return getattr(self.file, key)
