        class BZ2File(BufferedIOBase):
            def __init__(self, *args, **kwargs):
                self.__obj = bz2.BZ2File(*args, **kwargs)

            def close(self):
                return self.__obj.close()

            @property
            def closed(self):
                return self.__obj.closed

            def flush(self):
                pass

            def isatty(self):
                return self.__obj.isatty()

            def read(self, *args, **kwargs):
                return self.__obj.read(*args, **kwargs)

            def read1(self, *args, **kwargs):
                return self.__obj.read(*args, **kwargs)

            def readable(self):
                return 'r' in self.__obj.mode

            def readline(self, *args, **kwargs):
                return self.__obj.readline(*args, **kwargs)

            def readlines(self, *args, **kwargs):
                return self.__obj.readlines(*args, **kwargs)

            def seek(self, *args, **kwargs):
                self.__obj.seek(*args, **kwargs)
                return self.tell()

            def seekable(self):
                return self.readable()

            def tell(self):
                return self.__obj.tell()

            def truncate(self, *args, **kwargs):
                return self.__obj.truncate(*args, **kwargs)

            def writable(self):
                return 'w' in self.__obj.mode

            def write(self, *args, **kwargs):
                return self.__obj.write(*args, **kwargs)

            def writelines(self, *args, **kwargs):
                return self.__obj.writelines(*args, **kwargs)
