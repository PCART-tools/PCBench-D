    def __init__(self, write: str, access: str, type: str, **kwargs):
        self.write = write
        self.access = access
        self.type = type  # mime-type to send to S3.
