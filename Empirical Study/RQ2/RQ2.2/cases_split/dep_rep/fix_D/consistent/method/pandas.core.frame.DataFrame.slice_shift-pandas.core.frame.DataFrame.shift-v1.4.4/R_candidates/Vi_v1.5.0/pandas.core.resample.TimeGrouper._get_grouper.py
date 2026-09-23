    def _get_grouper(self, obj, validate: bool = True):
        # create the resampler and return our binner
        r = self._get_resampler(obj)
        return r.binner, r.grouper, r.obj
