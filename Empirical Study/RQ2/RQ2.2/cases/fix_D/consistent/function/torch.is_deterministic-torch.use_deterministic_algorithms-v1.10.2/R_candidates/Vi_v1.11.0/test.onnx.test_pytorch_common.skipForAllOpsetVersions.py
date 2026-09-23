def skipForAllOpsetVersions():
    def skip_dec(func):
        def wrapper(self):
            if self.opset_version:
                raise unittest.SkipTest("Skip verify test for unsupported opset_version")
            return func(self)
        return wrapper
    return skip_dec
