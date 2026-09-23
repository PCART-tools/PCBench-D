class HDFS3Wrapper(pa.filesystem.DaskFileSystem):
    """Wrapper around `hdfs3.HDFileSystem` that allows it to be passed to
    pyarrow methods"""
    def isdir(self, path):
        return self.fs.isdir(path)

    def isfile(self, path):
        return self.fs.isfile(path)
