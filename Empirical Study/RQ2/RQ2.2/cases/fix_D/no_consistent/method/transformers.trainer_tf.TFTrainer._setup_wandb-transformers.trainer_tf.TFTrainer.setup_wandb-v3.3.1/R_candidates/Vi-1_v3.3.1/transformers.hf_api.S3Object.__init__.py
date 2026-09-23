    def __init__(
        self,
        key: str,  # S3 object key
        etag: str,
        lastModified: str,
        size: int,
        rfilename: str,  # filename relative to config.json
        **kwargs
    ):
        self.key = key
        self.etag = etag
        self.lastModified = lastModified
        self.size = size
        self.rfilename = rfilename
        for k, v in kwargs.items():
            setattr(self, k, v)
