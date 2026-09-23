    @classmethod
    def schema_json(cls, *, by_alias=True, **dumps_kwargs) -> str:
        from .json import pydantic_encoder
        return json.dumps(cls.schema(by_alias=by_alias), default=pydantic_encoder, **dumps_kwargs)
