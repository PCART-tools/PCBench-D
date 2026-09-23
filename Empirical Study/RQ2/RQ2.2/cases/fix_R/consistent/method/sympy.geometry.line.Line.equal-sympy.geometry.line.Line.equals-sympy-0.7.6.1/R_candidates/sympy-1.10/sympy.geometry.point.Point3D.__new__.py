    def __new__(cls, *args, _nocheck=False, **kwargs):
        if not _nocheck:
            kwargs['dim'] = 3
            args = Point(*args, **kwargs)
        return GeometryEntity.__new__(cls, *args)
