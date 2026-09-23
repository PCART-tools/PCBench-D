    def load(self):
        loader = self._load()
        if loader is None:
            msg = f"cannot find loader for this {self.format} file"
            raise OSError(msg)
        image = loader.load(self)
        assert image is not None
        # become the other object (!)
        self.__class__ = image.__class__
        self.__dict__ = image.__dict__
        return image.load()
