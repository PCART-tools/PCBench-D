    def __init__(self, filename: str, LastModified: str, ETag: str, Size: int, **kwargs):
        self.filename = filename
        self.LastModified = LastModified
        self.ETag = ETag
        self.Size = Size
