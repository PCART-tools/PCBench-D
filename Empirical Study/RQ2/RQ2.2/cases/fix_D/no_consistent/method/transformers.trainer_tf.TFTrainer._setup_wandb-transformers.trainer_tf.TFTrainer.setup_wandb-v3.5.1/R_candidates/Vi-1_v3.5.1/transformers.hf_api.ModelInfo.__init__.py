    def __init__(
        self,
        modelId: Optional[str] = None,  # id of model
        author: Optional[str] = None,
        downloads: Optional[int] = None,
        tags: List[str] = [],
        pipeline_tag: Optional[str] = None,
        siblings: Optional[List[Dict]] = None,  # list of files that constitute the model
        **kwargs
    ):
        self.modelId = modelId
        self.author = author
        self.downloads = downloads
        self.tags = tags
        self.pipeline_tag = pipeline_tag
        self.siblings = [ModelSibling(**x) for x in siblings] if siblings is not None else None
        for k, v in kwargs.items():
            setattr(self, k, v)
