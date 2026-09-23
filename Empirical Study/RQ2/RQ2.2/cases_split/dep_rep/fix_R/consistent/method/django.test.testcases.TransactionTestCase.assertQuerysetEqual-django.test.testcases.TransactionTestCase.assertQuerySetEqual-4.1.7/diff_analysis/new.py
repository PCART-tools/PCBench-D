    def assertQuerysetEqual(self, *args, **kw):
        warnings.warn(
            "assertQuerysetEqual() is deprecated in favor of assertQuerySetEqual().",
            category=RemovedInDjango51Warning,
            stacklevel=2,
        )
        return self.assertQuerySetEqual(*args, **kw)
