    def __copy__(self, *args):
        raise NotImplementedError(
            "TransformNode instances can not be copied. "
            "Consider using frozen() instead.")
