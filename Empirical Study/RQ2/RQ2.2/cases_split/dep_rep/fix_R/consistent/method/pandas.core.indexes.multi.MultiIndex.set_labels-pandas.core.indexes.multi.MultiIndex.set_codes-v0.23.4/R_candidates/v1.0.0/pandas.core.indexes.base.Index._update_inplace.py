    def _update_inplace(self, result, **kwargs):
        # guard when called from IndexOpsMixin
        raise TypeError("Index can't be updated inplace")
