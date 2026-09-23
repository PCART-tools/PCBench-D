class PyArrowHadoopFileSystem(object):
    sep = "/"

    def __init__(self, **kwargs):
        self.fs = pa.hdfs.HadoopFileSystem(**kwargs)

    @classmethod
    def from_pyarrow(cls, fs):
        out = object.__new__(cls)
        out.fs = fs
        return out

    def open(self, path, mode='rb', **kwargs):
        return self.fs.open(path, mode=mode, **kwargs)

    def glob(self, path):
        return sorted(generic_glob(self.fs, posixpath, path))

    def mkdirs(self, path):
        return self.fs.mkdir(path, create_parents=True)

    def ukey(self, path):
        return tokenize(path, self.fs.info(path)['last_modified'])

    def size(self, path):
        return self.fs.info(path)['size']

    def _get_pyarrow_filesystem(self):
        return self.fs
