    def dict(self, *, include: Set[str]=None, exclude: Set[str]=set()) -> Dict[str, Any]:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
        """
        return {
            k: v for k, v in self
            if k not in exclude and (not include or k in include)
        }
