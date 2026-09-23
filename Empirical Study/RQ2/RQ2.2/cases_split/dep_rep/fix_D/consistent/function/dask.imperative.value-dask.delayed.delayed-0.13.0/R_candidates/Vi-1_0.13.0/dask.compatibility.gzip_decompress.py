    def gzip_decompress(b):
        f = gzip.GzipFile(fileobj=BytesIO(b))
        result = f.read()
        f.close()
        return result
