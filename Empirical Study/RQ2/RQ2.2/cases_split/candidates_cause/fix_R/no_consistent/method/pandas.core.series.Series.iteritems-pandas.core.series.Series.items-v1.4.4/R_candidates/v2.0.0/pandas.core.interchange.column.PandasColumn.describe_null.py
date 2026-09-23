    @property
    def describe_null(self):
        kind = self.dtype[0]
        try:
            null, value = _NULL_DESCRIPTION[kind]
        except KeyError:
            raise NotImplementedError(f"Data type {kind} not yet supported")

        return null, value
