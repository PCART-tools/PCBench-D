    def _update_inplace(self, result, **kwargs):
        # we want to call the generic version and not the IndexOpsMixin
        return generic.NDFrame._update_inplace(self, result, **kwargs)
