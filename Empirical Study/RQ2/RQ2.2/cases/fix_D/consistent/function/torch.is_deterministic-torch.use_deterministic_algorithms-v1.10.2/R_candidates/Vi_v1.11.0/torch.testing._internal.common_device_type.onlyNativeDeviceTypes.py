def onlyNativeDeviceTypes(fn):
    @wraps(fn)
    def only_fn(self, *args, **kwargs):
        if self.device_type not in NATIVE_DEVICES:
            reason = "onlyNativeDeviceTypes: doesn't run on {0}".format(self.device_type)
            raise unittest.SkipTest(reason)

        return fn(self, *args, **kwargs)

    return only_fn
