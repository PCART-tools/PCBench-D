    def json(self, *, include: Set[str]=None, exclude: Set[str]=set(), **dumps_kwargs) -> str:
        """
        Generate a JSON representation of the model, `include` and `exclude` arguments as per `dict()`. Other arguments
        as per `json.dumps()`.
        """
        from .json import pydantic_encoder
        return json.dumps(self.dict(include=include, exclude=exclude), default=pydantic_encoder, **dumps_kwargs)
