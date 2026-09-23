    def _get_grouper(self, obj):
        # create the resampler and return our binner
        r = self._get_resampler(obj)
        r._set_binner()
        return r.binner, r.grouper, r.obj
