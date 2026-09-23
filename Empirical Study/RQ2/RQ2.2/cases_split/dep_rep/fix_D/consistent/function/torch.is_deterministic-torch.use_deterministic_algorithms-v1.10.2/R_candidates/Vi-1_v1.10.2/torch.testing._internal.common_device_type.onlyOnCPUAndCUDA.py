def onlyOnCPUAndCUDA(fn):
    @wraps(fn)
    def only_fn(self, *args, **kwargs):
        if self.device_type != 'cpu' and self.device_type != 'cuda':
            reason = "onlyOnCPUAndCUDA: doesn't run on {0}".format(self.device_type)
            raise unittest.SkipTest(reason)

        return fn(self, *args, **kwargs)

    return only_fn
