    def values(self, *, include: Set[str]=None, exclude: Set[str]=set()) -> Dict[str, Any]:
        """
        Get a dict of the values processed by the model, optionally specifying which fields to include or exclude.

        This is NOT equivalent to the values() method on a dict.
        """
        return {
            k: v for k, v in self
            if k not in exclude and (not include or k in include)
        }
