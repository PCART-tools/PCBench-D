    def start(self, request):
        warnings.warn('use .prepare(request) instead', DeprecationWarning)
        # make pre-check to don't hide it by do_handshake() exceptions
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl

        parser, protocol, writer = self._pre_start(request)
        resp_impl = super().start(request)
        self._post_start(request, parser, protocol, writer)
        return resp_impl
