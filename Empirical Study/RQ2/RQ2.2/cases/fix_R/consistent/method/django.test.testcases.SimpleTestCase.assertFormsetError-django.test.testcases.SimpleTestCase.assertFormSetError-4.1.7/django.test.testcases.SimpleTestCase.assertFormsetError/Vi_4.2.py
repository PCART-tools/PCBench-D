    def assertFormsetError(self, *args, **kw):
        warnings.warn(
            "assertFormsetError() is deprecated in favor of assertFormSetError().",
            category=RemovedInDjango51Warning,
            stacklevel=2,
        )
        return self.assertFormSetError(*args, **kw)
