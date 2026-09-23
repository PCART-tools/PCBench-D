    def dict(self, *, include: Set[str]=None, exclude: Set[str]=set(), by_alias: bool = False) -> Dict[str, Any]:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
        """
        get_key = self._get_key_factory(by_alias)
        get_key = partial(get_key, self.fields)

        return {
            get_key(k): v
            for k, v in self._iter(by_alias=by_alias)
            if k not in exclude and (not include or k in include)
        }
