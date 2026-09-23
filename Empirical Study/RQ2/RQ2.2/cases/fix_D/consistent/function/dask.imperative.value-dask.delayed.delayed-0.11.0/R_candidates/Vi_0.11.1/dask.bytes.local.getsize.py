def getsize(path, compression=None):
    if compression is None:
        return os.path.getsize(path)
    else:
        with open(path, 'rb') as f:
            f = SeekableFile(f)
            g = seekable_files[compression](f)
            g.seek(0, 2)
            result = g.tell()
            g.close()
        return result
