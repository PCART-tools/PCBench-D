    def _guess_filename(self, obj):
        if isinstance(obj, io.IOBase):
            name = getattr(obj, 'name', None)
            if name is not None:
                return Path(name).name
