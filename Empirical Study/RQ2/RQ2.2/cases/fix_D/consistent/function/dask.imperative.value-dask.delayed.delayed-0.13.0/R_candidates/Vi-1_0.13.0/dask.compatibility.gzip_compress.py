    def gzip_compress(b):
        bio = BytesIO()
        f = gzip.GzipFile(fileobj=bio, mode='w')
        f.write(b)
        f.close()
        bio.seek(0)
        result = bio.read()
        return result
