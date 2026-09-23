class CaseInsensitiveMutableMultiDict(
        BaseMutableMultiDict, CaseInsensitiveMultiDict):
    """An ordered dictionary that can have multiple values for each key."""

    def getall(self, key, default=_marker):
        return super().getall(key.upper(), default)
