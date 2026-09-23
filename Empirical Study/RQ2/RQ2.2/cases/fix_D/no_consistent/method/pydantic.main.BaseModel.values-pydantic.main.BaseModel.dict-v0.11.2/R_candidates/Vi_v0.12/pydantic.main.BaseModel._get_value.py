    @classmethod
    def _get_value(cls, v, by_alias=False):
        if isinstance(v, BaseModel):
            return v.dict(by_alias=by_alias)
        elif isinstance(v, list):
            return [cls._get_value(v_, by_alias=by_alias) for v_ in v]
        elif isinstance(v, dict):
            return {k_: cls._get_value(v_, by_alias=by_alias) for k_, v_ in v.items()}
        elif isinstance(v, set):
            return {cls._get_value(v_, by_alias=by_alias) for v_ in v}
        elif isinstance(v, tuple):
            return tuple(cls._get_value(v_, by_alias=by_alias) for v_ in v)
        else:
            return v
