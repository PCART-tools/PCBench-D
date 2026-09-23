def skipIfUnsupportedOpsetVersion(unsupported_opset_versions):
    def skip_dec(func):
        def wrapper(self):
            if self.opset_version in unsupported_opset_versions:
                raise unittest.SkipTest("Skip verify test for unsupported opset_version")
            return func(self)
        return wrapper
    return skip_dec
