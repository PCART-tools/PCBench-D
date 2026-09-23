    def __add__(self, other):
        """
        Compose two transforms together so that *self* is followed by *other*.

        ``A + B`` returns a transform ``C`` so that
        ``C.transform(x) == B.transform(A.transform(x))``.
        """
        return (composite_transform_factory(self, other)
                if isinstance(other, Transform) else
                NotImplemented)
