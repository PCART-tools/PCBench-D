    def print_webp(self, filename_or_obj, *, metadata=None, pil_kwargs=None):
        self._print_pil(filename_or_obj, "webp", pil_kwargs, metadata)
