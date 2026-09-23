    class GzipFile(BufferedIOBase):
        def __init__(self, *args, **kwargs):
            self.__obj = gzip.GzipFile(*args, **kwargs)

        def close(self):
            return self.__obj.close()

        @property
        def closed(self):
            return self.__obj.fileobj is None

        def flush(self, *args, **kwargs):
            return self.__obj.flush(*args, **kwargs)

        def isatty(self):
            return self.__obj.isatty()

        def read(self, *args, **kwargs):
            return self.__obj.read(*args, **kwargs)

        def read1(self, *args, **kwargs):
            return self.__obj.read(*args, **kwargs)

        def readable(self):
            return self.__obj.mode == gzip.READ

        def readline(self, *args, **kwargs):
            return self.__obj.readline(*args, **kwargs)

        def readlines(self, *args, **kwargs):
            return self.__obj.readlines(*args, **kwargs)

        def seek(self, *args, **kwargs):
            self.__obj.seek(*args, **kwargs)
            return self.tell()

        def seekable(self):
            # See https://hg.python.org/cpython/file/2.7/Lib/gzip.py#l421
            return True

        def tell(self):
            return self.__obj.tell()

        def truncate(self, *args, **kwargs):
            return self.__obj.truncate(*args, **kwargs)

        def writable(self):
            return self.__obj.mode == gzip.WRITE

        def write(self, *args, **kwargs):
            return self.__obj.write(*args, **kwargs)

        def writelines(self, *args, **kwargs):
            return self.__obj.writelines(*args, **kwargs)
