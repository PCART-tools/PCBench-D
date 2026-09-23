def _nonzero_schemas():
    signatures = []

    def nonzero(self):
        pass
    signatures.append(inspect.signature(nonzero))

    def nonzero(self, *, as_tuple : bool):  # type: ignore[no-redef]
        pass
    signatures.append(inspect.signature(nonzero))

    return signatures
