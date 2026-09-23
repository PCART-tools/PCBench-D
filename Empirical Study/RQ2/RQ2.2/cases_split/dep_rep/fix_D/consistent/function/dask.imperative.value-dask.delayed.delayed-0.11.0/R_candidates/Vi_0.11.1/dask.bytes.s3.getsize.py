def getsize(path, compression, s3):
    if compression is None:
        return s3.info(path)['Size']
    else:
        with s3.open(path, 'rb') as f:
            g = seekable_files[compression](f)
            g.seek(0, 2)
            result = g.tell()
            g.close()
        return result
