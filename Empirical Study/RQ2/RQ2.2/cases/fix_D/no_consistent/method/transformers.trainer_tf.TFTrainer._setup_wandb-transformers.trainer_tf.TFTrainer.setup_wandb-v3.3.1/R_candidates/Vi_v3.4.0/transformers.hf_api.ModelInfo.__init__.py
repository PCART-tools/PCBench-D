    def __init__(
        self,
        modelId: str,  # id of model
        key: str,  # S3 object key of config.json
        author: Optional[str] = None,
        downloads: Optional[int] = None,
        tags: List[str] = [],
        pipeline_tag: Optional[str] = None,
        siblings: Optional[List[Dict]] = None,  # list of files that constitute the model
        **kwargs
    ):
        self.modelId = modelId
        self.key = key
        self.author = author
        self.downloads = downloads
        self.tags = tags
        self.pipeline_tag = pipeline_tag
        self.siblings = [S3Object(**x) for x in siblings] if siblings is not None else None
        for k, v in kwargs.items():
            setattr(self, k, v)
