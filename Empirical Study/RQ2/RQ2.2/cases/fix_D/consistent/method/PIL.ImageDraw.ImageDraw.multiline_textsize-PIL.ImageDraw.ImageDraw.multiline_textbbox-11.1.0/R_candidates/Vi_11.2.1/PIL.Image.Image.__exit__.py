    def __exit__(self, *args):
        from . import ImageFile

        if isinstance(self, ImageFile.ImageFile):
            if getattr(self, "_exclusive_fp", False):
                self._close_fp()
            self.fp = None
