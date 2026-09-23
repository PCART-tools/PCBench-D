    def start(self, request):
        warnings.warn('use .prepare(request) instead', DeprecationWarning)
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl

        return self._start(request)
